from datetime import date
import polars as pl
from google.cloud import bigquery
import io

from sa import credentials


schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("created_on", "TIMESTAMP"),
    bigquery.SchemaField("birth_date", "TIMESTAMP"),
    bigquery.SchemaField("microchip", "STRING"),
    bigquery.SchemaField("color", "STRING"),
    bigquery.SchemaField("breed", "STRING"),
    bigquery.SchemaField("photo_id", "STRING"),
    bigquery.SchemaField("likes", "INTEGER"),
    bigquery.SchemaField("dislikes", "INTEGER"),
    bigquery.SchemaField("votes", "INTEGER"),
    bigquery.SchemaField("id", "STRING"),
]

cat_user_schema = [
    bigquery.SchemaField("cat_id", "STRING"),
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("city", "STRING"),
]


def normalize_users_ids_column(
    column_name: str, cats_df: pl.DataFrame, users_df: pl.DataFrame
) -> pl.DataFrame:
    df_exploded = cats_df.explode(column_name)

    df_normalized = (
        df_exploded.select(
            [pl.col("id").alias("cat_id"), pl.col(column_name).alias("user_id")]
        )
        .join(
            users_df.rename({"id": "user_id"}),
            "user_id",
        )
        .select(
            [pl.col("cat_id"), pl.col("user_id"), pl.col("city"), pl.col("country")]
        )
    )

    return df_normalized


def upload_df_to_bigquery(
    client: bigquery.Client, df: pl.DataFrame, table: bigquery.Table
):
    with io.BytesIO() as stream:
        df.write_parquet(stream)
        stream.seek(0)
        job = client.load_table_from_file(
            stream,
            destination=table,
            job_config=bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.PARQUET,
            ),
        )
    job.result()


def load_data_to_big_query(cats_df: pl.DataFrame, users_df: pl.DataFrame) -> None:
    current_date = date.today()
    iso_calendar = current_date.isocalendar()

    table_name = f"voting_history_from_{iso_calendar.week}_{iso_calendar.year}_test16"
    biq_query_client = bigquery.Client(credentials=credentials)

    table_ref = biq_query_client.dataset("VotingHistoryDev").table(table_name)
    table = bigquery.Table(table_ref, schema=schema)
    table = biq_query_client.create_table(table)  # API request

    cats_df_users_dropped = cats_df.drop(
        ["likes_voted_users_ids", "dislikes_voted_users_ids"]
    )
    upload_df_to_bigquery(biq_query_client, cats_df_users_dropped, table)

    likes_df_normalized = normalize_users_ids_column(
        "likes_voted_users_ids", cats_df, users_df
    )

    likes_table_name = f"likes_{iso_calendar.week}_{iso_calendar.year}_test16"
    likes_table_ref = biq_query_client.dataset("VotingHistoryDev").table(
        likes_table_name
    )
    likes_table = bigquery.Table(likes_table_ref, schema=cat_user_schema)

    upload_df_to_bigquery(biq_query_client, likes_df_normalized, likes_table)

    dislikes_df_normalized = normalize_users_ids_column(
        "dislikes_voted_users_ids", cats_df, users_df
    )

    dislikes_table_name = f"dislikes_{iso_calendar.week}_{iso_calendar.year}_test16"
    dislikes_table_ref = biq_query_client.dataset("VotingHistoryDev").table(
        dislikes_table_name
    )
    dislikes_table = bigquery.Table(dislikes_table_ref, schema=cat_user_schema)

    upload_df_to_bigquery(biq_query_client, dislikes_df_normalized, dislikes_table)
