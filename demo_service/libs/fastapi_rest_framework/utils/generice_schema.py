from typing import Union
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel

from ..schemas import BaseSerializerSchemas, BaseResponseMode, BaseResponseListSchema


class GenericSchema:
    def __init__(self, model: BaseModel):
        self.model = model
        self.read_only = tuple(self.get_read_only_fields())

    def get_read_only_fields(self) -> list:
        return [
            field_name for field_name, field in self.model._meta.fields_map.items() if field.allows_generated
        ]

    def generate_meta(self, is_get: bool):
        class Meta:
            model = self.model
            is_many = is_get

        return Meta

    def generate_pydantic(self, is_get: bool):
        class PydanticModel:
            exclude = () if is_get else self.read_only

        return PydanticModel

    def generate_schema(
            self,
            suffix: str = "Schema",
            is_get: bool = True,
            is_schema_class: bool = True,
            super_class: PydanticModel = Union[BaseSerializerSchemas, BaseResponseMode, BaseResponseListSchema]
    ):
        schema_name = f"{self.model.__name__}{''.join([s.capitalize() for s in suffix.split('_')])}"
        schema_bases = (super_class,)
        schema_dict = {
            "Meta": self.generate_meta(is_get),
            "PydanticMeta": self.generate_pydantic(is_get),
        }

        schema_class = type(schema_name, schema_bases, schema_dict)
        return schema_class

    def init_schema(self, cls):
        schema_map = ("create", "list", "retrieve", "update", "destroy")

        for _map in schema_map:
            _class = self.generate_schema(
                suffix=f"{_map}_schema_class",
                is_get=True if _map in ["list", "retrieve"] else False,
                is_schema_class=True,
                super_class=cls.generic_schema
            )
            setattr(cls, f"{_map}_schema_class", _class)

        for _map in schema_map:
            _class = self.generate_schema(
                suffix=f"{_map}_response_model",
                is_get=True if _map in ["list", "retrieve"] else False,
                is_schema_class=False,
                super_class=BaseResponseListSchema if _map in ["list"] else BaseResponseMode
            )
            setattr(cls, f"{_map}_response_model", _class)
