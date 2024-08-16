from datetime import date

from models.cat_models import CatOfTheWeekCreate, CurrentRoundCatES
from queries.cat_queries import (
    select_all_nr_cats,
    delete_all_nr_cats,
    insert_cat_of_the_week,
)
from queries.user_queries import select_all_users
from es_queries.cat_es_queries import (
    delete_cats_with_votes,
    insert_es_current_round_cats,
    select_all_cats_with_votes,
)
from bigquery.operations import load_data_to_big_query
from utils.utils import list_of_pydantics_to_pl_df, find_winning_cat


async def round_end_logic():
    print("Job started")
    current_date = date.today()
    iso_calendar = current_date.isocalendar()

    # Select all Cats from ElasticSearch
    all_cats_with_votes_df = list_of_pydantics_to_pl_df(
        await select_all_cats_with_votes()
    )

    # Select all Users from FireStore
    all_users_df = list_of_pydantics_to_pl_df(await select_all_users())

    # Cat of the week finding
    winning_cat_df = find_winning_cat(all_cats_with_votes_df)
    winning_cat = winning_cat_df.to_dicts()[0]
    cat_of_the_week = CatOfTheWeekCreate(
        week_number=iso_calendar.week,
        year=iso_calendar.year,
        **winning_cat,
    )

    # Insert cat of the week to FireStore
    await insert_cat_of_the_week(cat_of_the_week)

    # Load to BigQuery Logic
    load_data_to_big_query(all_cats_with_votes_df, all_users_df)

    # Delete current round cats from ElasticSearch
    await delete_cats_with_votes()

    # Select all Next Round Cats from Firestore
    nr_cats = await select_all_nr_cats()

    # Create Current Round Cats for ElasticSearch
    current_round_cats = [CurrentRoundCatES(**cat.model_dump()) for cat in nr_cats]

    # Insert CRC to ES
    await insert_es_current_round_cats(current_round_cats)

    # Delete NRC from FireStore
    await delete_all_nr_cats(nr_cats)

    print("Job done")
