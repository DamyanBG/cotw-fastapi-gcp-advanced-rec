from datetime import date

from models.cat_models import (
    CurrentRoundCatCreate,
    CatOfTheWeekCreate,
)
from queries.cat_queries import (
    select_all_nr_cats,
    insert_current_round_cats,
    delete_all_nr_cats,
    select_winning_cat,
    insert_cat_of_the_week,
    delete_all_cr_cats,
    select_all_cr_cats_for_es,
)
from es_queries.cat_es_queries import (
    delete_cats_with_votes,
    insert_es_current_round_cats,
)


async def round_end_logic():
    print("Job started")
    winning_cat = await select_winning_cat()

    current_date = date.today()
    iso_calendar = current_date.isocalendar()
    cat_of_the_week = CatOfTheWeekCreate(
        week_number=iso_calendar.week,
        year=iso_calendar.year,
        **winning_cat.model_dump(),
    )
    await insert_cat_of_the_week(cat_of_the_week)
    await delete_all_cr_cats()
    await delete_cats_with_votes()

    nr_cats = await select_all_nr_cats()
    current_round_cats = [CurrentRoundCatCreate(**cat.model_dump()) for cat in nr_cats]
    await insert_current_round_cats(current_round_cats)
    crc_cats_for_es = await select_all_cr_cats_for_es()
    await insert_es_current_round_cats(crc_cats_for_es)
    await delete_all_nr_cats(nr_cats)
    print("Job done")
