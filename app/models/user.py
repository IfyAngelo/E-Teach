from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from bson import ObjectId

from core.utils import utcnow
from core.models import BaseModel, ModelPermission
from core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal


@dataclass
class User(BaseModel):
    email: str
    password: str
    username: str
    is_admin: bool = False
    created_at: Optional[datetime] = utcnow()
    updated_at: Optional[datetime] = utcnow()

    _collection_name_ = "ai_api_users"

    def __acl__(self):
        basic_permissions = [ModelPermission.READ, ModelPermission.CREATE]
        self_permissions = [
            ModelPermission.READ,
            ModelPermission.EDIT,
            ModelPermission.CREATE,
        ]
        all_permissions = list(ModelPermission)

        return [
            (Allow, Everyone, basic_permissions),
            (Allow, UserPrincipal(value=self.id), self_permissions),
            (Allow, RolePrincipal(value="admin"), all_permissions),
        ]