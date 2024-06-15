from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.column import ColumnSchemaRead, ColumnSchemaUpdate
from models.column import Column

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete



router = APIRouter(tags=["Column"])

@router.get("/boards/{board_id}/columns")
async def get_board_list(board_id: int, session: Annotated[Session, Depends(get_session)]): #-> list[ColumnSchemaRead]:""" 
    instances = session.scalars(select(Column).where(Column.board_id==board_id))
    return [instance.to_schema() for instance in instances]


@router.post("/boards/{board_id}/columns")
async def add_board(board_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchemaUpdate): #-> ColumnSchemaRead:
    instance = Column(board_id=board_id, **dict(column_schema))
    
    session.add(instance)
    session.commit()
    
    return instance.to_schema()
    

@router.get("/boards/{board_id}/columns/{column_id}")
async def get_board(board_id: int, column_id:int, session: Annotated[Session, Depends(get_session)]): #-> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return instance.to_schema()
    
    
@router.put("/boards/{board_id}/columns/{column_id}")
async def set_board(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchemaUpdate): #-> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(dict(column_schema))
    
    session.add(instance)
    session.commit()

    return instance.to_schema()


@router.delete("/boards/{board_id}/columns/{column_id}")
async def delete_board(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)]): #-> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Column).where(Column.id==column_id))
    session.commit()
    
    return instance.to_schema()


