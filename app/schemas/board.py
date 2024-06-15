from pydantic import BaseModel, Field


class BoardSchemaUpdate(BaseModel):
    title: str | None = Field(default="No name")
    description: str | None = Field(max_length=1000, default=None)
    avatar: str | None = Field(max_length=100, default=None)
    background: str | None = Field(max_length=100, default=None)
            
        
class BoardSchemaRead(BoardSchemaUpdate):
    id: int | None = Field(default=None)

    