from pydantic import BaseModel, Field
from schemas.card import CardSchemaRead


class ColumnSchemaUpdate(BaseModel):
    title: str | None = Field(max_length=100, default="No name")
          
class ColumnSchemaRead(ColumnSchemaUpdate):
    id: int
    board_id: int
    cards: list[CardSchemaRead]