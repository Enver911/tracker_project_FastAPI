from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class FollowerSchemaCreate(BaseModel):
    user_email: EmailStr = Field(max_length=30)
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaUpdate(BaseModel):
    permission: Literal["reader", "moderator"] = Field(default="reader")

class FollowerSchemaRead(FollowerSchemaCreate):
    id: int
    board_id: int
    

    