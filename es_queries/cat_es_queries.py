from asyncio import gather

from search import es, crc_index_name
from models.cat_models import CurrentRoundCatES


async def search_cat_for_vote(user_id: str) -> CurrentRoundCatES:
    query = {
        "query": {"bool": {"must_not": {"term": {"voted_users_ids": user_id}}}},
        "sort": [{"votes": {"order": "asc"}}],
        "size": 1,
        # "request_cache": False
    }

    response = await es.search(crc_index_name, body=query)
    cat_for_vote = CurrentRoundCatES(**response["hits"]["hits"][0]["_source"])

    return cat_for_vote


async def search_cat_by_id(cat_id: str) -> tuple[CurrentRoundCatES, str]:
    existing_cat_query = {"query": {"term": {"id": cat_id}}}
    result = await es.search(crc_index_name, body=existing_cat_query)
    crc_cat_doc = result["hits"]["hits"][0]
    crc_cat = CurrentRoundCatES(**crc_cat_doc["_source"])
    cat_doc_id = crc_cat_doc["_id"]

    return crc_cat, cat_doc_id


async def replace_cat(crc_cat: CurrentRoundCatES, crc_cat_doc_id):
    resp = await es.replace_document(
        crc_index_name, crc_cat.model_dump(), doc_id=crc_cat_doc_id
    )
    print(resp)


async def delete_cats_with_votes():
    await es.delete_all_documents(crc_index_name)


async def insert_es_current_round_cats(es_crc: list[CurrentRoundCatES]) -> None:
    load_cats_to_es_tasks = [
        es.insert_document(crc_index_name, cat.model_dump()) for cat in es_crc
    ]
    await gather(*load_cats_to_es_tasks)
