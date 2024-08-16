from fastapi import APIRouter, Depends, HTTPException, status

from models.vote_models import VoteData
from models.user_models import UserId
from auth.token import get_current_user_id
from queries.cat_queries import add_dislike, add_like
from utils.enums import VoteEnum
from es_queries.cat_es_queries import search_cat_by_id, replace_cat


votes_router = APIRouter(prefix="/vote", tags=["vote"])


@votes_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_vote(
    vote_data: VoteData, user_id: UserId = Depends(get_current_user_id)
):
    crc_cat, cat_doc_id = await search_cat_by_id(vote_data.cat_id)
    # print(crc_cat.voted_users_ids)

    if user_id.id in crc_cat.likes_voted_users_ids or user_id.id in crc_cat.dislikes_voted_users_ids: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already voted for this cat!",
        )

    
    crc_cat.votes = crc_cat.votes + 1

    if vote_data.vote == VoteEnum.Like:
        crc_cat.likes = crc_cat.likes + 1
        crc_cat.likes_voted_users_ids.append(user_id.id)
    else:
        crc_cat.dislikes = crc_cat.dislikes + 1
        crc_cat.dislikes_voted_users_ids.append(user_id.id)

    await replace_cat(crc_cat, cat_doc_id)

    return "OK"
