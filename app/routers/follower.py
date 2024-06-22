from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.db_depends import get_session

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from models.follower import Follower
from models.board import Board
from models.user import User

from schemas.follower import FollowerSchemaRead, FollowerSchemaCreate, FollowerSchemaUpdate


router = APIRouter(tags=["Follower"])


@router.get("/{board_id}/followers")
async def get_follower_list(board_id: int, session: Annotated[Session, Depends(get_session)]) -> list[FollowerSchemaRead]:
    instances = session.scalars(select(Follower).where(Follower.board_id==board_id))
    return [FollowerSchemaRead.model_validate(instance, from_attributes=True) for instance in instances]


@router.post("/{board_id}/followers")
async def get_follower_list(board_id: int, session: Annotated[Session, Depends(get_session)], follower_schema: FollowerSchemaCreate) -> FollowerSchemaRead:
    user = session.scalar(select(User).where(User.id==follower_schema.user_id))
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User wasn't found")
    
    board = session.scalar(select(Board).where(Board.id==board_id))
    
    if user in board.followers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already was followed to the board")
    elif user == board.author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That user is author of the board")
    
    instance = Follower(board_id=board_id, **dict(follower_schema))
    session.add(instance)
    session.commit()
    
    return FollowerSchemaRead.model_validate(instance, from_attributes=True)


@router.put("/{board_id}/followers/{follower_id}")
async def get_follower_list(board_id: int, follower_id: int, session: Annotated[Session, Depends(get_session)], follower_schema: FollowerSchemaUpdate) -> FollowerSchemaRead:
    instance = session.scalar(select(Follower).where(Follower.id==follower_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    instance.set(follower_schema.model_dump(exclude_unset=True))
    
    session.add(instance)
    session.commit()
    
    return FollowerSchemaRead.model_validate(instance, from_attributes=True)

@router.delete("/{board_id}/followers/{follower_id}")
async def get_follower_list(board_id: int, follower_id: int, session: Annotated[Session, Depends(get_session)]) -> FollowerSchemaRead:
    instance = session.scalar(select(Follower).where(Follower.id==follower_id))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query") 
    
    session.execute(delete(Follower).where(Follower.id==follower_id))
    session.commit()
    
    return FollowerSchemaRead.model_validate(instance, from_attributes=True)