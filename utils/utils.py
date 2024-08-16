import polars as pl
from pydantic import BaseModel


def separate_data_url_from_base64(base64_with_data_url: str) -> tuple[str, str]:
    data_url, base64_data = base64_with_data_url.split(",")
    return data_url, base64_data


def list_of_pydantics_to_pl_df(instances: list[BaseModel]) -> pl.DataFrame:
    df = pl.DataFrame(instances)
    return df


def find_winning_cat(cats_df: pl.DataFrame) -> pl.DataFrame:
    winning_cat = cats_df.with_columns(
        (pl.col("likes") - pl.col("dislikes")).alias("diff")
    ).sort("diff", descending=True).head(1)
    return winning_cat
