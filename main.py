from elasticsearch import Elasticsearch
from mapping import Mapping
from uuid import UUID
import json
from loader import IndexLoader
from config import ES
from typing import Optional

class Client:
    map_instance = Mapping(params={'uuid': UUID, 'title': str, 'description': str, 'template': str, 'is_public': bool })
    mapping = map_instance.generate_mapping()
    def __init__(self, url: str = ES.URL) -> None:
        self.es = Elasticsearch([url], verify_certs=False)
        self.loader = IndexLoader(self.es)

    def load_index(self, path: Optional[str] = ES.INDEX.PATH, name: Optional[str] = ES.INDEX.NAME):
        with open(path, 'r', encoding='utf-8') as file:
            index_settings = json.load(file)
        self.loader.create_mapping(name, index_settings)        

client = Client()
client.load_index()