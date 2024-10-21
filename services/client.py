from elasticsearch import Elasticsearch
from services.mapping import Mapping
import json
from services.loader import IndexLoader
from config import ES
from typing import Optional, Dict
from services.files import FileSystem as fs
from services.query import RandomQuery

class Client:
    map_instance = Mapping(params={'id': int, 'title': str, 'description': str, 'template': str, 'is_public': bool })
    mapping = map_instance.generate_mapping()
    def __init__(self, url: str = ES.URL) -> None:
        self.es = Elasticsearch([url], verify_certs=False)
        self.loader = IndexLoader(self.es)
        self.query = RandomQuery(self.mapping)

    def index_create(self, name: Optional[str] = ES.INDEX.NAME, path: Optional[str] = ES.INDEX.PATH) -> None:
        index_settings = fs.parse_json(path)
        self.loader.create_mapping(name, index_settings)       

    def index_delete(self, index_name: Optional[str] = ES.INDEX.NAME) -> bool:
        return self.loader.delete_index(index_name) 

    def index_reload(self, index_name: Optional[str] = ES.INDEX.NAME) -> None:
        if self.loader.is_exists(index_name):
            self.doc_delete_all(index_name)
        self.index_delete(index_name)
        self.index_create(index_name)

    def doc_add(self, index_name: Optional[str] = ES.INDEX.NAME, data: Optional[Dict[str, str]] = {}) -> None:
        if data == {}: data = self.query.generate_document(index_name)
        fs.create_doc(index_name, data)
        self.es.index(index=index_name, id=data['id'], body=data)

    def doc_count(self, index_name: Optional[str] = ES.INDEX.NAME) -> int:
        result = self.es.count(index=index_name)
        return int(result["count"])
    
    def doc_delete_all(self, index_name: Optional[str] = ES.INDEX.NAME) -> int:
        result = self.es.delete_by_query(index=index_name, query={"match_all": {}})
        fs.delete_docs(index_name)
        return int(result['deleted'])
    
    def search_simple(self, search_text: str, index_name: Optional[str] = ES.INDEX.NAME) -> list:
        query = {
            "query": {
                "multi_match": {
                    "query": search_text,
                    "fields": ["title^2", "description"],
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            },
            "size": 10,
            "from": 0
        }

        response = self.es.search(index=index_name, body=query)
        return response['hits']['hits']
    
    def anylize(self, index_name: Optional[str] = ES.INDEX.NAME, body: Optional[dict[str, str]] = {}) -> dict[str, str]: 
        return self.es.indices.analyze(index=index_name, body=body)
    
    def format_output(self, response: object) -> None:
        print(json.dumps(response, ensure_ascii=False, indent=4))

    def upload_test_data(self):
        test_data = fs.get_dir('test')
        for data in test_data:
            self.doc_add(ES.INDEX.NAME, data)

    def test_queries(self):
        test_cases = {
            "око": ["1f9d0af1-a702-41bd-82d0-b7c3826f78be"],
            # добавь другие запросы и соответствующие id
        } 
        results = {}
    
        for query, relevant_ids in test_cases.items():
            response = self.es.search(index=ES.INDEX.NAME, body={
                "query": {
                    "match": {
                        "title": query
                    }
                }
            })
            
            found_ids = [hit['_id'] for hit in response['hits']['hits']]
            results[query] = {
                "relevant": relevant_ids,
                "found": found_ids
            }
        return results