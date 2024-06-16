from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.board import BoardSchemaRead, BoardSchemaUpdate
from models.board import Board

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete



router = APIRouter(tags=["Board"])


@router.get("/boards")
async def get_board_list(session: Annotated[Session, Depends(get_session)]) -> list[BoardSchemaRead]:
    instances = session.scalars(select(Board)).all()
    return [BoardSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/boards")
async def add_board(session: Annotated[Session, Depends(get_session)], board_schema: BoardSchemaUpdate) -> BoardSchemaRead:
    data = board_schema.model_dump(exclude="id")
    instance = Board(**data)
    
    session.add(instance)
    session.commit()

    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.get("/boards/{board_id}")
async def get_board(board_id: int, session: Annotated[Session, Depends(get_session)]) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)
    
    
@router.put("/boards/{board_id}")
async def set_board(board_id: int, session: Annotated[Session, Depends(get_session)], board_schema: BoardSchemaUpdate) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(board_schema.model_dump(exclude="id", exclude_unset=True))
    
    session.add(instance)
    session.commit()

    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/boards/{board_id}")
async def delete_board(board_id: int, session: Annotated[Session, Depends(get_session)]) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Board).where(Board.id==board_id))
    session.commit()
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)


