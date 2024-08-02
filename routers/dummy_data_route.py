from fastapi import APIRouter
from aiofiles import open as asopen
from datetime import date
import asyncio
import base64
import random

from models.image_models import ImageFileName
from queries.user_queries import insert_user
from queries.image_queries import insert_image
from queries.cat_queries import (
    insert_current_round_cats,
    insert_nrc,
    insert_cat_of_the_week,
)
from queries.batch_queries import insert_batch_users
from storage.google_cloud_storage import upload_bytes_image
from utils.image_compression import compress_image_to_webp
from utils.utils import separate_data_url_from_base64
from dummy_data.data_creators import (
    create_dummy_user,
    create_dummy_nrc,
    create_dummy_crc,
    create_dummy_cotw,
)

dummy_data_router = APIRouter(prefix="/load-dummy-data", tags=["dummy", "test", "data"])


async def create_dummy_data(number_to_create):
    # Create dummy users
    user_creates = [create_dummy_user() for _ in range(number_to_create)]
    users = await insert_batch_users(user_creates)

    # Create and upload dummy images for cats
    cat_images_file_names = []
    for _ in range(1, number_to_create):
        image_number = random.randint(1, 3)
        async with asopen(
            f"dummy_data/images/cat_image_{image_number}.webp", "rb"
        ) as f:
            image_data = await f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        base64_with_data_url = f"data:image/webp;base64,{image_base64}"

        image_bytes = compress_image_to_webp(
            separate_data_url_from_base64(base64_with_data_url)[1]
        )
        image_file_name = upload_bytes_image(image_bytes, ".webp", "image/webp")
        cat_images_file_names.append(ImageFileName(file_name=image_file_name))

    insert_image_tasks = [
        insert_image(image_name) for image_name in cat_images_file_names
    ]
    images = await asyncio.gather(*insert_image_tasks)

    # Create dummy current round cats
    crc_creates = [
        create_dummy_crc(user.id, image.id) for user, image in zip(users, images)
    ]
    await insert_current_round_cats(crc_creates)

    # Create dummy next round cat
    nrc_create = create_dummy_nrc(users[3].id, images[1].id)
    await insert_nrc(nrc_create)

    # Create and upload dummy image for Cat of the Week
    async with asopen("dummy_data/images/cat_of_the_week.webp", "rb") as f:
        image_data = await f.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    base64_with_data_url = f"data:image/webp;base64,{image_base64}"

    image_bytes = compress_image_to_webp(
        separate_data_url_from_base64(base64_with_data_url)[1]
    )
    cofw_image_file_name = upload_bytes_image(image_bytes, ".webp", "image/webp")
    cotw_image = await insert_image(ImageFileName(file_name=cofw_image_file_name))

    # Create dummy Cat of the Week
    current_date = date.today()
    iso_calendar = current_date.isocalendar()
    cotw_create = create_dummy_cotw(users[-1].id, cotw_image.id)
    cotw_create.year = iso_calendar.year
    cotw_create.week_number = iso_calendar.week

    await insert_cat_of_the_week(cotw_create)


@dummy_data_router.post("/")
async def load_dummy_data():
    number_to_create = 20

    tasks = []
    for _ in range(4):
        tasks.append(create_dummy_data(number_to_create))

    await asyncio.gather(*tasks)

    return "OK"
