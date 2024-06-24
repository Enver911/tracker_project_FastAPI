from fastapi import APIRouter, Depends, UploadFile
from fastapi import HTTPException, status

from schemas.board import BoardSchemaRead, BoardSchemaUpdate
from models.board import Board

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from models.user import User

import settings
from utils.media import Media

from permissions.permissions import is_author_or_moderator, is_author
from authentications.jwt_auth import get_user

from sqlalchemy.orm import joinedload


router = APIRouter(tags=["Board"])


@router.get("/boards")
async def get_board_list(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> list[BoardSchemaRead]: 
    user = session.scalar(select(User).options(joinedload(User.boards, Board.author), 
                                               joinedload(User.boards, Board.followers),
                                               joinedload(User.follows, Board.author),
                                               joinedload(User.follows, Board.followers)).where(User.id==user_info["id"]))
                                               
                                         
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")
       
    instances = user.boards + user.follows
    
    return [BoardSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/boards")
async def add_board(session: Annotated[Session, Depends(get_session)], board_schema: BoardSchemaUpdate, user_info: Annotated[dict, Depends(get_user)]) -> BoardSchemaRead:
    instance = Board(**board_schema.model_dump())
    instance.author_id = user_info["id"]
    
    session.add(instance)
    session.commit()

    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.get("/boards/{board_id}", dependencies=[Depends(is_author_or_moderator)])
async def get_board(board_id: int, session: Annotated[Session, Depends(get_session)]) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)
    
    
@router.put("/boards/{board_id}", dependencies=[Depends(is_author_or_moderator)])
async def set_board(board_id: int, session: Annotated[Session, Depends(get_session)], board_schema: BoardSchemaUpdate) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(board_schema.model_dump(exclude_unset=True))
    
    session.add(instance)
    session.commit()

    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/boards/{board_id}", dependencies=[Depends(is_author)])
async def delete_board(board_id: int, session: Annotated[Session, Depends(get_session)]) -> BoardSchemaRead:
    instance = session.scalar(select(Board).where(Board.id==board_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Board).where(Board.id==board_id))
    session.commit()
    
    return BoardSchemaRead.model_validate(instance, from_attributes=True)


@router.post("/boards/{board_id}/media", dependencies=[Depends(is_author_or_moderator)])
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


@router.delete("/boards/{board_id}/media", dependencies=[Depends(is_author_or_moderator)])
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