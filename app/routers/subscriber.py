from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.db_depends import get_session

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from models.subscriber import Subscriber
from models.board import Board
from models.user import User
from models.card import Card
from models.follower import Follower

from schemas.subscriber import SubscriberSchemaRead, SubscriberSchemaUpdate


router = APIRouter(tags=["Subscriber"])


@router.get("/{board_id}/cards/{card_id}/subscribers")
async def get_follower_list(board_id: int, card_id: int, session: Annotated[Session, Depends(get_session)]) -> list[SubscriberSchemaRead]:
    instances = session.scalars(select(Subscriber).where(Subscriber.card_id==card_id))
    return [SubscriberSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/{board_id}/cards/{card_id}/subscribers")
async def get_follower_list(board_id: int, card_id: int, session: Annotated[Session, Depends(get_session)], subscriber_schema: SubscriberSchemaUpdate) -> SubscriberSchemaRead:
   
    board = session.scalar(select(Board).where(Board.id==board_id))
    board_users = board.followers + [board.author]
    
    user = session.scalar(select(User).where(User.email==subscriber_schema.user_email))
    
    if user is None or user not in board_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User wasn't found")
    
    card = session.scalar(select(Card).where(Card.id==card_id))
    
    if card is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No matches for given query")
    
    if user in card.subscribers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already was subscribed to the card")
    
    instance = Subscriber(card_id=card_id, **dict(subscriber_schema))
    session.add(instance)
    session.commit()
    
    return SubscriberSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/{board_id}/subscribers/{subscriber_id}")
async def get_follower_list(board_id: int, subscriber_id: int, session: Annotated[Session, Depends(get_session)]) -> SubscriberSchemaRead:
    
    instance = session.scalar(select(Subscriber).where(Subscriber.id==subscriber_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Subscriber).where(Subscriber.id==subscriber_id))
    session.commit()
    
    return SubscriberSchemaRead.model_validate(instance, from_attributes=True)