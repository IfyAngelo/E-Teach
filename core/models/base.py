from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Any, Dict
from bson import ObjectId


class ModelPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


@dataclass
class BaseModel:
    """Base class for MongoDB models."""
    id: ObjectId = field(default_factory=ObjectId, init=False)

    def to_dict(self) -> dict:
        """
        Convert the model instance to a dictionary.

        :return: A dictionary representation of the model.
        """
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}

    # @abstractmethod
    # def __acl__(self) -> list[tuple[type, object, list[ModelPermission]]]:
    #     """
    #     Define access control rules for the model.
    #
    #     :return: A list of access control rules.
    #     """
    #     raise NotImplementedError
