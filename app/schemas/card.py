from pydantic import BaseModel, Field
from datetime import datetime


class CardSchemaUpdate(BaseModel):
    title: str | None = Field(max_length=100, default="No name")
    description: str | None = Field(max_length=1000, default=None)
    avatar: str | None = Field(max_length=100, default=None)
    background: str | None = Field(max_length=100, default=None)
    deadline: datetime | None = None
    
    
class CardSchemaRead(CardSchemaUpdate):
    id: int
    column_id: int
    created: datetime
    updated: datetime
 