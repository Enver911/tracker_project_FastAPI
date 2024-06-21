from pydantic import BaseModel, Field
from schemas.column import ColumnSchemaRead
from schemas.user import UserSchemaPublicInfo


class BoardSchemaUpdate(BaseModel):
    title: str | None = Field(default="No name")
    description: str | None = Field(max_length=1000, default=None)
    background: str | None = Field(max_length=100, default=None)
            
        
class BoardSchemaRead(BoardSchemaUpdate):
    id: int
    avatar: str | None = Field(max_length=100, default=None)
    author: UserSchemaPublicInfo
    
