from typing import TypeVar, Generic, Type, List, Optional

from pydantic import BaseModel
from tortoise import Model

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        实现数据库持久层基类
        增删改查操作
        :param model:
        """
        self.model = model

    async def get(self, model_id: int) -> Optional[Model]:
        """
        查询一条数据
        :param model_id:
        :return:
        """
        return await self.model.filter(id=model_id).first()

    async def get_multi(self, *, skip=0, limit=10, **kwargs) -> List[ModelType]:
        """
        查询多条数据 分页
        :param skip:
        :param limit:
        :param kwargs:
        :return:
        """
        return await self.model.filter(**kwargs).offset(skip).limit(limit).order_by("-id").all()

    async def get_multi_count(self, **kwargs) -> int:
        """
        分页查询获取总数
        :param kwargs:
        :return:
        """
        return await self.model.filter(**kwargs).count()

    async def get_all(self, **kwargs) -> List[ModelType]:
        """
        查询有数据
        :return:
        """
        return await self.model.filter(**kwargs).all()

    async def get_one(self, **kwargs) -> ModelType:
        """
        查询一条数据
        :return:
        """
        return await self.model.filter(**kwargs).first()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        添加数据
        :param obj_in:
        :return:
        """
        obj_in_data = obj_in.dict(skip_defaults=True)
        return await self.model.create(**obj_in_data)

    async def update(self, obj_in: UpdateSchemaType, **kwargs) -> int:
        """
        更新数据
        :param obj_in:
        :return:
        """
        obj_in_data = obj_in.dict(skip_defaults=True)
        return await self.model.filter(**kwargs).update(**obj_in_data)

    async def remove(self, *, model_id: int) -> int:
        """
        删除一条数据
        :param model_id:
        :return:
        """
        return await self.model.filter(id=model_id).delete()

    async def count(self) -> int:
        """
        查询条数
        :return:
        """
        return await self.model.all().count()

    async def filter_count(self, **kwargs) -> int:
        """
        根据条件，查询条数
        :return:
        """
        return await self.model.filter(**kwargs).all().count()
