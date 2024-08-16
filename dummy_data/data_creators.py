from faker import Faker
import random

from models.user_models import UserCreate
from models.cat_models import (
    NextRoundCatCreate,
    CurrentRoundCatCreate,
    CatOfTheWeekCreate,
)

fake = Faker()

country_city_mapping = {
    "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool"],
    "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Palermo"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Japan": ["Tokyo", "Osaka", "Nagoya", "Sapporo", "Fukuoka"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
    "Bulgaria": ["Sofia", "Dobrich", "Burgas"],
}

CAT_BREEDS = [
    "Abyssinian",
    "American Shorthair",
    "Bengal",
    "Birman",
    "British Shorthair",
    "Burmese",
    "Chartreux",
    "Cornish Rex",
    "Devon Rex",
    "Egyptian Mau",
    "Exotic Shorthair",
    "Himalayan",
    "Japanese Bobtail",
    "Maine Coon",
    "Manx",
    "Norwegian Forest Cat",
    "Oriental Shorthair",
    "Persian",
    "Ragdoll",
    "Russian Blue",
    "Scottish Fold",
    "Siamese",
    "Siberian",
    "Singapura",
    "Somali",
    "Sphynx",
    "Tonkinese",
    "Turkish Angora",
    "Turkish Van",
]


def create_dummy_user() -> UserCreate:
    country = random.choice(list(country_city_mapping.keys()))
    city = random.choice(country_city_mapping[country])

    return UserCreate(
        **{
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "city": city,
            "country": country,
        }
    )


def create_dummy_nrc(user_id: str, image_id: str) -> NextRoundCatCreate:
    return NextRoundCatCreate(
        **{
            "name": fake.first_name(),
            "user_id": user_id,
            "color": fake.color_name(),
            "breed": random.choice(CAT_BREEDS),
            "birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
            "microchip": fake.ean(length=8),
            "photo_id": image_id,
        }
    )


def create_dummy_crc(user_id: str, image_id: str) -> CurrentRoundCatCreate:
    return CurrentRoundCatCreate(
        **{
            "name": fake.first_name(),
            "color": fake.color_name(),
            "breed": random.choice(CAT_BREEDS),
            "birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
            "microchip": fake.ean(length=8),
            "photo_id": image_id,
            "user_id": user_id,
        }
    )


def create_dummy_cotw(user_id: str, image_id: str) -> CatOfTheWeekCreate:
    return CatOfTheWeekCreate(
        **{
            "photo_id": image_id,
            "user_id": user_id,
            "name": fake.first_name(),
            "color": fake.color_name(),
            "breed": random.choice(CAT_BREEDS),
            "birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
            "microchip": fake.ean(length=8),
            "likes": fake.random_int(min=0, max=100),
            "dislikes": fake.random_int(min=0, max=10),
            "votes": fake.random_int(min=0, max=110),
            "week_number": fake.random_int(min=0, max=50),
            "year": fake.random_int(min=2015, max=2024),
        }
    )
