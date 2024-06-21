from pydantic import BaseModel, Field
from datetime import datetime

from schemas.user import UserSchemaPublicInfo


class CardSchemaUpdate(BaseModel):
    title: str | None = Field(max_length=100, default="No name")
    description: str | None = Field(max_length=1000, default=None)
    background: str | None = Field(max_length=100, default=None)
    deadline: datetime | None = None
    

class CardSchemaRead(CardSchemaUpdate):
    id: int
    column_id: int
    avatar: str | None = Field(max_length=100, default=None)
    created: datetime
    updated: datetime
    subscribers: list[UserSchemaPublicInfo]
