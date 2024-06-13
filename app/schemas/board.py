from pydantic import BaseModel, Field
from sqlalchemy import inspect


class BoardSchema(BaseModel):
    id: int | None = Field(default=None)
    title: str | None = Field(default="No name")
    description: str | None = None
    avatar: str | None = None
    background: str | None = Field(max_length=100, default=None)
    
    @classmethod
    def from_model(cls, instance):
        return cls(**{attr.key: attr.value for attr in inspect(instance).attrs})
            
        

    