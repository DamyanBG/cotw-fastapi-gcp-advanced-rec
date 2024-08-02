from typing import Mapping
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError

from config import ELASTIC_HOST

crc_index_name = "current-round-cats"

crc_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "created_on": {"type": "date"},
            "birth_date": {"type": "date"},
            "microchip": {"type": "keyword"},
            "color": {"type": "keyword"},
            "breed": {"type": "keyword"},
            "photo_id": {"type": "keyword"},
            "likes": {"type": "integer"},
            "dislikes": {"type": "integer"},
            "votes": {"type": "integer"},
            "id": {"type": "keyword"},
            "voted_users_ids": {"type": "keyword"}
        }
    }
}


class Search:
    _connected: bool = True

    def __init__(self) -> None:
        try:
            self._es = AsyncElasticsearch(ELASTIC_HOST)
            
        except ConnectionError:
            self._connected = False
            print("Can't connect to ElasticSearch")

    async def check_index_exists(self, index_name: str) -> bool:
        index_exists = await self._es.indices.exists(index=index_name)
        return index_exists
    
    async def list_all_indices(self):
        indices = await self._es.indices.get_alias(index="*")
        print(indices)

    async def create_index(self, index_name: str, mapping: Mapping):
        return await self._es.indices.create(index=index_name, body=mapping)

    async def delete_index(self, index_name: str) -> None:
        await self._es.indices.delete(index=index_name)

    async def insert_document(self, index_name: str, document: dict):
        return await self._es.index(index=index_name, body=document)
    
    async def replace_document(self, index_name: str, document: dict, doc_id: str):
        return await self._es.index(index=index_name, body=document, id=doc_id)
    
    async def update_document(self, index_name, doc_id, document):
        await self._es.update(index=index_name, id=doc_id, body=document)
    
    async def create_index_if_not_exists(self, index_name: str, mapping: Mapping) -> None:
        index_exists = await self.check_index_exists(index_name=index_name)
        if index_exists:
            print(f"Index {index_name} exists.")
        else:
            print(f"Index {index_name} does not exists. Attempt for creating will be executed!")
            resp = await self.create_index(index_name=index_name, mapping=mapping)
            print(type(resp))
            print(resp)

    async def delete_all_documents(self, index_name):
        query = {
            "query": {
                "match_all": {}
            }
        }

        await self._es.delete_by_query(index=index_name, body=query)
    
    async def search(self, index_name: str, **query_args):
        if self._connected:
            return await self._es.search(index=index_name, **query_args)
        return None
    

es = Search()