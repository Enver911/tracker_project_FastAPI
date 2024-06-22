from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from authentications.jwt_auth import get_user

from backend.db_depends import get_session

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.board import Board
from models.follower import Follower, PERMISSIONS
from models.user import User


SAFE_METHODS = ['GET', 'OPTIONS', 'HEAD']


async def is_author_or_moderator(request: Request, board_id: int, session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> dict:
    board = session.scalar(select(Board).where(Board.id==board_id))
    
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query")
    
    print(board.__dict__)
    
    follower = session.scalar(select(Follower).where(Follower.user_id==user_info["id"], Follower.board_id==board_id))
    
    if request.method in SAFE_METHODS:
        if board.author.id == user_info["id"] or follower: # if author or follower
            return user_info
    else:
        if board.author.id == user_info["id"] or (follower and follower.permission==PERMISSIONS["moderator"]): # if author or follower-moderator
            return user_info

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")


async def is_author(request: Request, board_id: int, session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> dict:
    board = session.scalar(select(Board).where(Board.id==board_id))
    
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matches for given query")
   
    if board.author.id == user_info["id"]: # is author
        return user_info

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")