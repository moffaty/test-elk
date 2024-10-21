from typing import Any

from elasticsearch import Elasticsearch

from config import ES

class IndexLoader:
    def __init__(self, search: Elasticsearch) -> None:
        self.__search = search

    def create_mapping(self, index_name: str, body: dict[str, Any]) -> None:
        if not self.__search.indices.exists(index=index_name):
            self.__search.indices.create(index=index_name, body=body)

    def delete_index(self, index_name: str) -> None:
        if self.__search.indices.exists(index=index_name):
            self.__search.indices.delete(index=index_name)

    def upload_index_data(self, data: list[dict[str, Any]]) -> None:
        self.__search.bulk(body=data, request_timeout=ES.REQUEST_TIMEOUT)

    def delete_index_document(self, index_name: str, document_id: int) -> None:
        self.__search.delete(index=index_name, id=document_id)

    def is_exists(self, index_name: str) -> bool:
        return self.__search.indices.exists(index=index_name)