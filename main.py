from elasticsearch import Elasticsearch
from services.mapping import Mapping
from uuid import UUID
import json
from services.loader import IndexLoader
from config import ES
from typing import Optional, Dict
from services.files import FileSystem as fs
from services.query import RandomQuery

class Client:
    map_instance = Mapping(params={'id': UUID, 'title': str, 'description': str, 'template': str, 'is_public': bool })
    mapping = map_instance.generate_mapping()
    def __init__(self, url: str = ES.URL) -> None:
        self.es = Elasticsearch([url], verify_certs=False)
        self.loader = IndexLoader(self.es)
        self.query = RandomQuery(self.mapping)

    def load_index(self, path: Optional[str] = ES.INDEX.PATH, name: Optional[str] = ES.INDEX.NAME) -> None:
        index_settings = fs.parse_json(path)
        self.loader.create_mapping(name, index_settings)        

    def fill_index(self, index_name: Optional[str] = ES.INDEX.NAME, data: Optional[Dict[str, str]] = {}) -> None:
        if data == {}: data = self.query.generate_document(index_name)
        fs.create_doc(index_name, data)
        self.es.index(index=index_name, id=data['id'], body=data)

    def docs_count(self, index_name: Optional[str] = ES.INDEX.NAME) -> int:
        result = self.es.count(index=index_name)
        return int(result["count"])
    
    def delete_all_docs(self, index_name: Optional[str] = ES.INDEX.NAME) -> int:
        result = self.es.delete_by_query(index=index_name, query={"match_all": {}})
        fs.delete_docs(index_name)
        return int(result['deleted'])
    

client = Client()
client.delete_all_docs()
# for _ in range(10):
#     (client.fill_index())