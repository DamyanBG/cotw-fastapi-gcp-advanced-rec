from typing import Iterable

from db import db
from models.user_models import UserCreate, User
from queries.user_queries import user_ref


async def insert_batch_users(users: Iterable[UserCreate]) -> list[User]:
    asbatch = db.batch()
    created_users = []
    for user in users:
        new_user_ref = user_ref.document()
        user_dict = user.model_dump()
        asbatch.set(new_user_ref, user_dict)
        created_users.append(User(
            id=new_user_ref.id, **user_dict
        ))

    await asbatch.commit()
    return created_users
