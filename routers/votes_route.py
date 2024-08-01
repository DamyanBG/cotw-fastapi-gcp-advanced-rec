from fastapi import APIRouter, Depends, HTTPException, status

from models.vote_models import Vote, VoteCreate, VoteData
from models.user_models import UserId
from auth.token import get_current_user_id
from queries.cat_queries import add_dislike, add_like
from utils.enums import VoteEnum


votes_router = APIRouter(prefix="/vote", tags=["vote"])


@votes_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_vote(
    vote_data: VoteData, user_id: UserId = Depends(get_current_user_id)
):
    # existing_vote = await select_vote_by_cat_and_user(vote_data.cat_id, user_id.id)
    # if existing_vote:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You already voted for this cat!",
    #     )

    # vote_create_data = VoteCreate(user_id=user_id.id, cat_id=vote_data.cat_id)
    # vote = await insert_vote(vote_create_data)

    if vote_data.vote == VoteEnum.Like:
        await add_like(vote_data.cat_id, user_id.id)
    else:
        await add_dislike(vote_data.cat_id, user_id.id)

    return "OK"
