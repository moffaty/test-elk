from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Dict, Optional, Type, Any, Literal, Union

class Mapping(BaseModel):
    params: Optional[Dict[str, Type]] = {}

    def generate_mapping(self) -> Dict[str, Any]:
        type_mapping = {
            str: 'text',
            bool: 'boolean',
            int: 'int',
            UUID: 'uuid'
        }
        return {field: type_mapping.get(field_type, 'unknown') for field, field_type in self.params.items()}
