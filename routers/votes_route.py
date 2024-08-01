from fastapi import APIRouter, Depends, HTTPException, status

from models.vote_models import Vote, VoteCreate, VoteData
from models.user_models import UserId
from models.cat_models import CurrentRoundCatES
from auth.token import get_current_user_id
from queries.vote_queries import insert_vote, select_vote_by_cat_and_user
from queries.cat_queries import add_dislike, add_like
from utils.enums import VoteEnum
from search import es, crc_index_name


votes_router = APIRouter(prefix="/vote", tags=["vote"])

async def update_voted_users(es, index_name, doc_id, user_id):
    script = {
        "script": {
            "source": """
                if (ctx._source.voted_users == null) {
                    ctx._source.voted_users = [params.user_id];
                } else if (!ctx._source.voted_users.contains(params.user_id)) {
                    ctx._source.voted_users.add(params.user_id);
                }
            """,
            "lang": "painless",
            "params": {
                "user_id": user_id
            }
        }
    }

    response = await es.update(index=index_name, id=doc_id, body=script)
    return response


@votes_router.post("/", status_code=status.HTTP_201_CREATED)
async def post_vote(
    vote_data: VoteData, user_id: UserId = Depends(get_current_user_id)
):
    existing_cat_query = {
        "query": {
            "term": {
                "id": vote_data.cat_id  # Assuming `cat_id` is stored in the `id` field
            }
        }
    }
    result = await es.search(crc_index_name, body=existing_cat_query)
    crc_cat_doc = result["hits"]["hits"][0]
    crc_cat = CurrentRoundCatES(**crc_cat_doc["_source"])
    
    print(crc_cat.voted_users_ids)

  
    crc_cat.voted_users_ids.append(user_id.id)


    await es.replace_document(crc_index_name, crc_cat.model_dump(), doc_id=crc_cat_doc["_id"])
    

    if vote_data.vote == VoteEnum.Like:
        await add_like(crc_cat.id)
    else:
        await add_dislike(crc_cat.id)

    return "OK"
