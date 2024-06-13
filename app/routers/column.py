from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.column import ColumnSchema
from models.column import Column

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete



router = APIRouter(tags=["Column"])

@router.get("/boards/{board_id}/columns")
async def get_board_list(board_id: int, session: Annotated[Session, Depends(get_session)]) -> list[ColumnSchema]:
    instances = session.scalars(select(Column).where(Column.board_id==board_id))
    return [ColumnSchema.from_model(instance) for instance in instances]


@router.post("/boards/{board_id}/columns")
async def add_board(board_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchema) -> ColumnSchema:
    data = column_schema.model_dump(exclude=["id", "board_id"])
    instance = Column(board_id=board_id, **data)
    
    session.add(instance)
    session.commit()
    
    return ColumnSchema.from_model(instance)
    

@router.get("/boards/{board_id}/columns/{column_id}")
async def get_board(board_id: int, column_id:int, session: Annotated[Session, Depends(get_session)]) -> ColumnSchema:
    instance = session.scalar(select(Column).where(Column.board_id==board_id, Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return ColumnSchema.from_model(instance)
    
    
@router.put("/boards/{board_id}/columns/{column_id}")
async def set_board(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchema) -> ColumnSchema:
    instance = session.scalar(select(Column).where(Column.board_id==board_id, Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(column_schema.model_dump(exclude=["id", "board_id"]))
    
    session.add(instance)
    session.commit()

    return ColumnSchema.from_model(instance)


@router.delete("/boards/{board_id}/columns/{column_id}")
async def delete_board(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)]) -> ColumnSchema:
    instance = session.scalar(select(Column).where(Column.board_id==board_id, Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Column).where(Column.board_id==board_id, Column.id==column_id))
    session.commit()
    
    return ColumnSchema.from_model(instance)


