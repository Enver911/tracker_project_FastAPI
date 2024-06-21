from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.column import ColumnSchemaRead, ColumnSchemaUpdate
from models.column import Column

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete


router = APIRouter(tags=["Column"])

@router.get("/{board_id}/columns")
async def get_column_list(board_id: int, session: Annotated[Session, Depends(get_session)])-> list[ColumnSchemaRead]: 
    instances = session.scalars(select(Column).where(Column.board_id==board_id))
    return [ColumnSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/{board_id}/columns")
async def add_column(board_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchemaUpdate) -> ColumnSchemaRead:
    instance = Column(board_id=board_id, **dict(column_schema))
    
    session.add(instance)
    session.commit()
    
    return ColumnSchemaRead.model_validate(instance, from_attributes=True)
    

@router.get("/{board_id}/columns/{column_id}")
async def get_column(board_id: int, column_id:int, session: Annotated[Session, Depends(get_session)]) -> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return ColumnSchemaRead.model_validate(instance, from_attributes=True)
    
    
@router.put("/{board_id}/columns/{column_id}")
async def set_column(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)], column_schema: ColumnSchemaUpdate) -> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(column_schema.model_dump(exclude_unset=True))
    
    session.add(instance)
    session.commit()

    return ColumnSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/{board_id}/columns/{column_id}")
async def delete_column(board_id: int, column_id: int, session: Annotated[Session, Depends(get_session)]) -> ColumnSchemaRead:
    instance = session.scalar(select(Column).where(Column.id==column_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Column).where(Column.id==column_id))
    session.commit()
    
    return ColumnSchemaRead.model_validate(instance, from_attributes=True)


