from datetime import datetime
from pydantic import BaseModel, Field


class BaseCatModel(BaseModel):
    name: str
    created_on: datetime = Field(default_factory=datetime.now)
    birth_date: datetime
    microchip: str
    color: str
    breed: str
    photo_id: str


class CatImageURL(BaseModel):
    image_url: str


class NextRoundCatBase(BaseCatModel):
    pass


class NextRoundCatData(NextRoundCatBase):
    pass


class NextRoundCatCreate(NextRoundCatBase):
    user_id: str


class NextRoundCat(NextRoundCatBase):
    id: str
    user_id: str


class NextRoundCatWithImage(NextRoundCat, CatImageURL):
    pass


class NextRoundCatUpdate(NextRoundCatBase):
    id: str


class CurrentRoundCatBase(BaseCatModel):
    likes: int = 0
    dislikes: int = 0
    votes: int = 0


class CurrentRoundCatCreate(CurrentRoundCatBase):
    pass


class CurrentRoundCat(CurrentRoundCatBase):
    id: str


class CurrentRoundCatWithImage(CurrentRoundCat, CatImageURL):
    pass


class CatOfTheWeekBase(BaseCatModel):
    likes: int
    dislikes: int
    votes: int
    week_number: int
    year: int


class CatOfTheWeekCreate(CatOfTheWeekBase):
    pass


class CatOfTheWeek(CatOfTheWeekBase):
    id: str


class CatOfTheWeekWithImage(CatOfTheWeek, CatImageURL):
    pass