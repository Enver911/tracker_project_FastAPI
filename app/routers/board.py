from fastapi import APIRouter, Depends, UploadFile
from fastapi import HTTPException, status

from schemas.board import BoardSchemaRead, BoardSchemaUpdate
from models.board import Board

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from authentications.jwt_auth import get_user
from models.user import User
from models.follower import Follower

import settings
from utils.media import Media

import os
import glob

router = APIRouter(tags=["Board"])


@router.get("/boards")
async def get_board_list(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> list[BoardSchemaRead]:
    user = session.scalar(select(User).where(User.email==user_info["email"]))
    instances = user.boards + user.follows
    return [BoardSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/boards")
async def add_board(session: Annotated[Session, Depends(get_session)], board_schema: BoardSchemaUpdate, user_info: Annotated[dict, Depends(get_user)]) -> BoardSchemaRead:
    instance = Board(**board_schema.model_dump())
    instance.author_email = user_info["email"]
    
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
    
    instance.set(board_schema.model_dump(exclude_unset=True))
    
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


@router.post("/boards/{board_id}/media")
async def set_board(board_id: int, session: Annotated[Session, Depends(get_session)], avatar: UploadFile) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query")
    
    file_path = f"{settings.STATICFILES_DIR}/boards/{board_id}/avatar/{avatar.filename}" 
    Media.save(avatar.file, path=file_path)
    
    instance.avatar = file_path
    session.add(instance)
    session.commit()
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/boards/{board_id}/media")
async def set_board(board_id: int, session: Annotated[Session, Depends(get_session)]) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query")
    
    file_path = f"{settings.STATICFILES_DIR}/boards/{board_id}/avatar/" 
    Media.clean(path=file_path)
    
    instance.avatar = None
    session.add(instance)
    session.commit()
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)