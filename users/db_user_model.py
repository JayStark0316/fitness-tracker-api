import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from commons.utils.app_utils import utc_now
from users.user_enums import UserRole


class UserDbModel(BaseModel):
    id: Optional[UUID] = Field(alias='_id',default_factory=uuid4)
    email: str = Field(min_length=5, max_length=400, description="Encrypted email address associated with the user")
    hashed_email: str = Field(description="Hashed email address for the user identification")
    display_name: Optional[str] = Field(default=None, description="User display name")
    password: str = Field(description="Hashed password for the user")
    role: str = Field(default=UserRole.USER, description="User role")
    created_on: datetime = Field(default_factory= utc_now)
    updated_on: datetime = Field(default_factory= utc_now, on_update=utc_now)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
