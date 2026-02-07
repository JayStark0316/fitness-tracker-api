from datetime import datetime,timezone
from typing import Optional

from pydantic import BaseModel, Field


class DefaultApiErrorResponse(BaseModel):
    message: str
    status_code: int
    timestamp: str = Field(default_factory=lambda: str(datetime.now(timezone.utc)))
    reasons:Optional[list] = Field(default_factory=list)