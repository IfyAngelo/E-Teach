from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from core.database import Propagation, Transactional
from core.models.base import BaseModel
from core.exceptions import NotFoundException
from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseController(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: Type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_id(self, id_: int) -> ModelType:
        """
        Returns the model instance matching the id.

        :param id_: The id to match.
        :return: The model instance.
        """
        db_obj = await self.repository.get_by(field="id", value=id_, unique=True)
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
            )
        return db_obj

    async def get_by_uuid(self, uuid: UUID) -> ModelType:
        """
        Returns the model instance matching the uuid.

        :param uuid: The uuid to match.
        :return: The model instance.
        """
        db_obj = await self.repository.get_by(field="uuid", value=uuid, unique=True)
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {uuid} does not exist"
            )
        return db_obj

    async def get_all(
            self, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :return: A list of records.
        """

        response = await self.repository.get_all(skip, limit)
        return response

    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """
        Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.
        :return: The created object.
        """
        create = await self.repository.create(attributes)
        return create

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(self, model: ModelType) -> None:
        """
        Deletes the Object from the DB.

        :param model: The model to delete.
        :return: True if the object was deleted, False otherwise.
        """
        delete = await self.repository.delete(model)
        return delete

    @staticmethod
    async def extract_attributes_from_schema(
            schema: BaseModel, excludes: set = None
    ) -> dict[str, Any]:
        """
        Extracts the attributes from the schema.

        :param schema: The schema to extract the attributes from.
        :param excludes: The attributes to exclude.
        :return: The attributes.
        """

        return await schema.dict(exclude=excludes, exclude_unset=True)