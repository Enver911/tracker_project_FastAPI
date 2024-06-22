from pydantic import BaseModel, Field
from typing import Literal


class FollowerSchemaCreate(BaseModel):
    user_id: int
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaUpdate(BaseModel):
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaRead(FollowerSchemaCreate):
    id: int
    board_id: int
    

    