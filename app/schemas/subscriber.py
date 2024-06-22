from pydantic import BaseModel, Field
from schemas.user import UserSchemaPublicInfo

class SubscriberSchemaUpdate(BaseModel):
    username: str = Field(max_length=30)

class SubscriberSchemaRead(BaseModel):
    id: int
    card_id: int
    user: UserSchemaPublicInfo