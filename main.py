from elasticsearch import Elasticsearch
from mapping import Mapping
from uuid import UUID
import json
from loader import IndexLoader
from config import ES
from typing import Optional, Dict
from query import RandomQuery

class Client:
    map_instance = Mapping(params={'uuid': UUID, 'title': str, 'description': str, 'template': str, 'is_public': bool })
    mapping = map_instance.generate_mapping()
    def __init__(self, url: str = ES.URL) -> None:
        self.es = Elasticsearch([url], verify_certs=False)
        self.loader = IndexLoader(self.es)
        self.query = RandomQuery(self.mapping)

    def load_index(self, path: Optional[str] = ES.INDEX.PATH, name: Optional[str] = ES.INDEX.NAME) -> None:
        with open(path, 'r', encoding='utf-8') as file:
            index_settings = json.load(file)
        self.loader.create_mapping(name, index_settings)        

    def fill_index(self, index_name: Optional[str] = ES.INDEX.NAME, data: Optional[Dict[str, str]] = {}) -> None:
        if data == {}: data = self.query.generate_document(index_name)
        self.loader.upload_index_data(data)

    def count(self, index_name: Optional[str] = ES.INDEX.NAME):
        result = self.es.count(index=index_name)
        return int(result["count"])
