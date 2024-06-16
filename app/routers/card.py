from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.card import CardSchemaUpdate, CardSchemaRead
from models.card import Card

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete



router = APIRouter(tags=["Card"])

@router.get("/boards/{board_id}/columns/{column_id}/cards")
async def get_card_list(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)]) -> list[CardSchemaRead]:
    instances = session.scalars(select(Card).where(Card.column_id==column_id))
    return [CardSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/boards/{board_id}/columns/{column_id}/cards")
async def add_card(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)], card_schema: CardSchemaUpdate) -> CardSchemaRead:
    instance = Card(column_id=column_id, **dict(card_schema))
    
    session.add(instance)
    session.commit()
    
    return CardSchemaRead.model_validate(instance, from_attributes=True)
    

@router.get("/boards/{board_id}/columns/{column_id}/cards/{card_id}")
async def get_card(board_id: int, column_id:int, card_id: int, session: Annotated[Session, Depends(get_session)]) -> CardSchemaRead:
    instance = session.scalar(select(Card).where(Card.id==card_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return CardSchemaRead.model_validate(instance, from_attributes=True)
    
    
@router.put("/boards/{board_id}/columns/{column_id}/cards/{card_id}")
async def set_card(board_id: int, column_id: int, card_id: int, session: Annotated[Session, Depends(get_session)], card_schema: CardSchemaUpdate) -> CardSchemaRead:
    instance = session.scalar(select(Card).where(Card.id==card_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(card_schema.model_dump(exclude_unset=True))
    
    session.add(instance)
    session.commit()

    return CardSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/boards/{board_id}/columns/{column_id}/cards/{card_id}")
async def delete_card(board_id: int, column_id: int, card_id: int, session: Annotated[Session, Depends(get_session)]) -> CardSchemaRead:
    instance = session.scalar(select(Card).where(Card.id==card_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Card).where(Card.id==card_id))
    session.commit()
    
    return CardSchemaRead.model_validate(instance, from_attributes=True)


