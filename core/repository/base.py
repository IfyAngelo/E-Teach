from typing import Any, Generic, Type, TypeVar
from pydantic import BaseModel
# from core.models import BaseModel
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType], db_session: AsyncIOMotorClientSession):
        self.session = db_session
        self.collection: AsyncIOMotorCollection = db_session.client.db[model._collection_name_]
        self.model_class: Type[ModelType] = model

    async def create(self, attributes: dict[str, Any] = None) -> ModelType:
        """
        Creates the model instance.

        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        inserted = await self.collection.insert_one(model.to_dict(), session=self.session)
        model.id = inserted.inserted_id
        return model

    async def get_all(
            self, skip: int = 0, limit: int = 100, sort: dict | None = None, filter_dict: dict | None = None
    ) -> list[ModelType]:
        """
        Returns a list of model instances from the database.

        :param skip: The number of documents to skip (offset).
        :param limit: The maximum number of documents to return.
        :param sort: A dictionary specifying sort criteria (e.g., {"field": "asc"}).
        :param filter_dict: Optional filter dictionary for complex queries
        :return: A list of model instances.
        """

        if filter_dict is None:
            filter_dict = {}
        # Use Motor's find with skip and limit options
        cursor = self.collection.find(filter_dict, skip=skip, limit=limit)

        # Apply sort criteria if provided
        if sort:
            sort_options = {key: value for key, value in sort.items()}
            cursor = cursor.sort(sort_options)

        # Fetch documents and convert to model instances
        documents = await cursor.to_list(length=limit)
        return [self.model_class.from_dict(doc) for doc in documents]

    async def get_by(
            self,
            field: str,
            value: Any,
            sort: dict | None = None,
            unique: bool = True,
    ) -> ModelType | list[ModelType]:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param sort: A dictionary specifying sort criteria (e.g., {"field": "asc"}).
        :param unique: If True, returns only the first matching document.
        :return: A model instance or list of model instances (None if not found).
        """
        # Build filter dictionary
        filter_dict = {field: value}

        # Use Motor's find with filter and optional sort
        cursor = self.collection.find(filter_dict)
        if sort:
            sort_options = {key: value for key, value in sort.items()}
            cursor = cursor.sort(sort_options)

        # Fetch document and convert to model instance
        if unique:
            document = await cursor.to_list(length=1)  # Limit to 1 document

            return self.model_class.from_dict(document[0]) if document else None
        else:
            documents = await cursor.to_list(length=None)
            return [self.model_class.from_dict(doc) for doc in documents] if documents else None

    async def delete(self, model: ModelType) -> None:
        """
        Deletes the model instance from the database.

        :param model: The model instance to delete.
        :return: None
        """
        # Get the ID from the model instance
        model_id = getattr(model, "id")  # Assuming "id" is the field for the document ID
        # Use Motor's delete_one with the ID filter
        await self.collection.delete_one({"_id": model_id}, session=self.session)

    async def update(self, model: ModelType, update_data: dict[str, Any]) -> ModelType:
        """
        Updates a model instance in the database.

        :param model: The model instance to update.
        :param update_data: A dictionary containing the update data.
        :return: The updated model instance.
        """
        # Get the ID from the model instance
        model_id = getattr(model, "id")

        # Use Motor's update_one with the ID filter and update data
        await self.collection.update_one({"_id": model_id}, {"$set": update_data}, session=self.session)

        # Refetch the updated document to return a complete model instance
        updated_doc = await self.get_by(field='_id', value=model_id)
        return updated_doc