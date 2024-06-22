from pydantic import BaseModel, Field
from typing import Literal
from schemas.user import UserSchemaPublicInfo

class FollowerSchemaCreate(BaseModel):
    username: str = Field(max_length=30)
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaUpdate(BaseModel):
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaRead(BaseModel):
    id: int
    board_id: int
    user: UserSchemaPublicInfo
    permission: Literal["reader", "moderator"] = Field(default="reader")
    

    