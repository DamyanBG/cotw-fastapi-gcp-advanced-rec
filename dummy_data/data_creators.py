from faker import Faker

from models.user_models import UserCreate
from models.cat_models import NextRoundCatCreate, CurrentRoundCatCreate, CatOfTheWeekCreate

fake = Faker()

def create_dummy_user() -> UserCreate:
    return UserCreate(**{
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password()
    })


def create_dummy_nrc(user_id: str, image_id: str) -> NextRoundCatCreate:
    return NextRoundCatCreate(**{
        "name": fake.first_name(),
        "user_id": user_id,
        "color": fake.color_name(),
        "breed": fake.word(),  # Faker does not have breed generation, using a random word instead
        "birth_date": fake.date_of_birth().strftime('%Y-%m-%d'),
        "microchip": fake.ean(length=8),
        "photo_id": image_id
    })


def create_dummy_crc(user_id: str, image_id: str) -> CurrentRoundCatCreate:
    return CurrentRoundCatCreate(**{
        "name": fake.first_name(),
        "color": fake.color_name(),
        "breed": fake.word(),  # Faker does not have breed generation, using a random word instead
        "birth_date": fake.date_of_birth().strftime('%Y-%m-%d'),
        "microchip": fake.ean(length=8),
        "photo_id": image_id,
        "user_id": user_id,
    })


def create_dummy_cotw(user_id: str, image_id: str) -> CatOfTheWeekCreate:
    return CatOfTheWeekCreate(**{
        "photo_id": image_id,
        "user_id": user_id,
        "name": fake.first_name(),
        "color": fake.color_name(),
        "breed": fake.word(),  # Faker does not have breed generation, using a random word instead
        "birth_date": fake.date_of_birth().strftime('%Y-%m-%d'),
        "microchip": fake.ean(length=8),
        "likes": fake.random_int(min=0, max=100),
        "dislikes": fake.random_int(min=0, max=10),
        "votes": fake.random_int(min=0, max=110),
        "week_number": fake.random_int(min=0, max=50),
        "year": fake.random_int(min=2015, max=2024),
    })
