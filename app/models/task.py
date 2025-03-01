from bson import ObjectId
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from core.utils import utcnow
from core.models.base import BaseModel, ModelPermission
from core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


@dataclass
class Task(BaseModel):
    _collection_name_ = "ai_api_task"

    title: str
    description: str
    task_author_id: ObjectId

    is_completed: bool = False
    created_at: Optional[datetime] = utcnow()
    updated_at: Optional[datetime] = utcnow()

    def __acl__(self):
        basic_permissions = [ModelPermission.CREATE]
        self_permissions = [
            ModelPermission.READ,
            ModelPermission.EDIT,
            ModelPermission.DELETE,
        ]
        all_permissions = list(ModelPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.task_author_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]