from pydantic import BaseModel, Field
from sqlalchemy import inspect


class ColumnSchema(BaseModel):
    id: int | None = None
    board_id: int | None = None
    title: str | None = Field(default="No name")
    
    @classmethod
    def from_model(cls, instance):
        return cls(**{attr.key: attr.value for attr in inspect(instance).attrs})
            
        

    