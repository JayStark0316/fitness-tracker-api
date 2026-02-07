from typing import Optional

from pydantic import BaseModel, Field

class RequestCreateUserSchema(BaseModel):
    """
    Schema for creating a user request.

    This class serves as a data validation model for creating a new user. It enforces
    constraints on the fields to ensure the data is formatted correctly and meets
    the required specifications.

    :ivar email: The email address of the user. Must have a minimum length of 5
        and a maximum length of 400 characters.
    :type email: str
    :ivar password: The password for the user account. Must have a minimum length
        of 8 characters.
    :type password: str
    :ivar display_name: The display name of the user. Must have a minimum length
        of 3 and a maximum length of 20 characters.
    :type display_name: str
    """
    email: str = Field(min_length=5, max_length=400)
    password: str = Field(min_length=8)
    display_name: str = Field(min_length=3, max_length=20)


class ResponseUserSchema(BaseModel):
    """
    Represents the schema for a user response.

    This class defines the structure used to represent a user's data in responses.
    It includes attributes such as the user's unique identifier, display name, and
    timestamps indicating when the user was created or last updated.

    :ivar id: Unique identifier of the user.
    :type id: str
    :ivar display_name: Display name of the user. Defaults to None if not provided.
    :type display_name: Optional[str]
    :ivar created_on: Timestamp representing when the user was created.
    :type created_on: str
    :ivar update_on: Timestamp representing when the user was last updated.
    :type update_on: str
    """
    id: str
    display_name: Optional[str] = Field(default=None)
    created_on: str
    update_on: str
