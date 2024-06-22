from pydantic import BaseModel


class SubscriberSchemaUpdate(BaseModel):
    user_id: int

class SubscriberSchemaRead(SubscriberSchemaUpdate):
    id: int
    card_id: int