import uuid
import json
from typing import Union, Dict
from faker import Faker
from config import ES
from services.mapping import Mapping

class RandomQuery:
    def __init__(self, mapping: dict[str, str]) -> None:
        self.__fake_generator = Faker(['ru_RU', 'en_US'])
        self.__mapping: dict[str, str] = mapping
        self.id = 0

    def generate_value(self, field_type: str) -> Union[str, bool, int, None]:
        generation_methods = {
            'id': self.get_id,
            'text': self.generate_text,
            'boolean': self.__fake_generator.boolean,
            'int': self.generate_int,
        }
        return generation_methods.get(field_type, lambda: None)()
    
    def get_id(self) -> int:
        self.id += 1
        return self.id

    def generate_int(self) -> str:
        return self.__fake_generator.random_int(min=0, max=100)

    def generate_text(self, count_of_sentence: int = ES.COUNT_OF_SENTENCE) -> str:
        russian_text = " ".join([self.__fake_generator.sentence() for _ in range(count_of_sentence)])
        return russian_text
    
    def generate_document(self, index_name: str) -> Dict[str, Union[str, bool, int]]:
        document = {}
        for field, field_type in self.__mapping.items():
            document[field] = self.generate_value(field_type)
        return document  
        