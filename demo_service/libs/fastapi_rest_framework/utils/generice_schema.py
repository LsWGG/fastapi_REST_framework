from typing import Union

from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel

from ..schemas import BaseSerializerSchemas, BaseResponseMode, BaseResponseListSchema


class GenericSchema:
    def __init__(self, model: Model):
        self.model = model
        self.generated_field = tuple(self.get_generated_fields())

    def get_generated_fields(self) -> list:
        return [
            field_name for field_name, field in self.model._meta.fields_map.items() if field.allows_generated
        ]

    def generate_meta(self, many: bool):
        class Meta:
            model = self.model
            is_many = many

        return Meta

    def generate_pydantic(self, read_only: bool):
        class PydanticMeta:
            exclude = () if read_only else self.generated_field

        return PydanticMeta

    def generate_schema(
            self,
            suffix: str = "Schema",
            many: bool = False,
            read_only: bool = False,
            super_class: PydanticModel = Union[BaseSerializerSchemas, BaseResponseMode, BaseResponseListSchema],
    ):
        # todo: 生成有问题
        schema_name = f"{self.model.__name__}{''.join([s.capitalize() for s in suffix.split('_')])}"
        schema_bases = (super_class,)
        schema_dict = {
            "__module__": self.__module__,
            "Meta": self.generate_meta(many=many),
            "PydanticMeta": self.generate_pydantic(read_only=read_only),
        }
        schema_class = type(schema_name, schema_bases, {})
        setattr(schema_class, "Meta", self.generate_meta(many=many))
        setattr(schema_class, "PydanticMeta", self.generate_pydantic(read_only=read_only))
        return schema_class

    def init_schema(self, cls):
        # Schema类：请求参数校验
        cls.schema_class = self.generate_schema(
            suffix=f"schema_class",
            read_only=True,
            super_class=cls.generic_schema
        )

        base_schema = self.generate_schema(
            suffix=f"base_schema",
            super_class=cls.generic_schema
        )
        cls.create_schema_class = None
        cls.update_schema_class = None

        # 响应模型：定义响应格式
        cls.response_model = BaseResponseMode

        list_base_schema = self.generate_schema(
            suffix=f"list_base_schema",
            many=True,
            read_only=True,
            super_class=cls.generic_schema
        )

        class ResponseListAuthorSchema(BaseResponseListSchema):
            class ListData(BaseModel):
                data: Union[None, list_base_schema()]
                count: int

            data: ListData

        cls.list_response_model = ResponseListAuthorSchema

        class ResponseRetrieveSchema(BaseResponseMode):
            data: Union[None, cls.schema_class()]

        cls.retrieve_response_model = ResponseRetrieveSchema

        # schema_map = ("create", "list", "retrieve", "update", "destroy")
        #
        # for _map in schema_map:
        #     _class = self.generate_schema(
        #         suffix=f"{_map}_schema_class",
        #         is_get=True if _map in ["list", "retrieve"] else False,
        #         is_schema_class=True,
        #         super_class=cls.generic_schema
        #     )
        #     setattr(cls, f"{_map}_schema_class", _class)
        #
        # for _map in schema_map:
        #     _class = self.generate_schema(
        #         suffix=f"{_map}_response_model",
        #         is_get=True if _map in ["list", "retrieve"] else False,
        #         is_schema_class=False,
        #         super_class=BaseResponseListSchema if _map in ["list"] else BaseResponseMode
        #     )
        #     setattr(cls, f"{_map}_response_model", _class)
