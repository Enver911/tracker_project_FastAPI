from pydantic import BaseModel, EmailStr, Field


class SubscriberSchemaUpdate(BaseModel):
    user_email: EmailStr = Field(max_length=30)

class SubscriberSchemaRead(SubscriberSchemaUpdate):
    id: int
    card_id: int