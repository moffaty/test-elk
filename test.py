from services.client import Client
from services.files import FileSystem as fs
from config import ES
if __name__ == "__main__":
    class TestClient:
        client = Client()
        def upload_test_data(self):
            test_data = fs.get_dir('test')
            for data in test_data:
                self.client.doc_add(ES.INDEX.NAME, data, False)

        def test_title(self):
            test_cases = {
                "fol": ["1", "4"],
                "win": ["2", "6"],
                "дор": ["3", "10"],
                "aff": ["4", "1"],
                "пок": ["5", "8"],
                "age": ["6", "2"],
                "wri": ["7", "5"],
                "gre": ["8", "10"],
                "pop": ["9", "6"],
                "own": ["10", "3"],
                # добавь другие запросы и соответствующие id
            } 
            results = {}
        
            for query, relevant_ids in test_cases.items():
                response = self.client.es.search(index=ES.INDEX.NAME, body={
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
        
    test = TestClient()
    test.client.format_output(test.test_title())