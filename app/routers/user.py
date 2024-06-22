from fastapi import APIRouter, Depends, HTTPException, status, UploadFile

from schemas.user import UserSchemaCreate, UserSchemaRead, UserSchemaPasswordReset, UserSchemaUpdate
from authentications.jwt_auth import JWT
from models.user import User

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, Delete

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime
from jose import jwt

from utils.media import Media

import settings

from authentications.jwt_auth import get_user


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["User"])


@router.post("/users/registration")
async def user_registration(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaCreate) -> UserSchemaRead:

    if session.scalar(select(User).where(or_(User.username==user_schema.username, User.email==user_schema.email))): # if user exists 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    user_schema.password = bcrypt_context.hash(user_schema.password)
    instance = User(**dict(user_schema))
    
    session.add(instance)
    session.commit()
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)

"""
@router.post("/users/password_reset")
async def user_password_reset(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaPasswordReset): 
    pass
"""

@router.post("/users/login")
async def user_login(session: Annotated[Session, Depends(get_session)], credentials: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JWT:
    instance = (session.scalar(select(User).where(User.username==credentials.username)) or
                session.scalar(select(User).where(User.email==credentials.username)))
    
    if not instance or not bcrypt_context.verify(credentials.password, instance.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username/email or password", headers={"WWW-Authenticate": "Bearer"})
    
    expires = (datetime.now() + settings.ACCESS_TOKEN_LIFETIME).timestamp()
    encode_dict = {"id": instance.id, "username": instance.username, "email": instance.email, "expires": expires}
    
    token = jwt.encode(claims=encode_dict, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return JWT(access_token=token)


@router.get("/users/profile")
async def some_url(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.id==user_info["id"]))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.put("/users/profile")
async def some_url(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)], user_schema: UserSchemaUpdate) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.id==user_info["id"]))
   
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")

    model_dump = user_schema.model_dump(exclude_unset=True)
    model_dump_username = model_dump.get("username")
    model_dump_email = model_dump.get("email")
    
    if (model_dump_username and 
        instance.username != model_dump_username and 
        session.scalar(select(User).where(User.username==model_dump_username))):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    if (model_dump_email and 
        instance.email != model_dump_email and 
        session.scalar(select(User).where(User.email==model_dump_email))):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    instance.set(model_dump)
    
    session.add(instance)
    session.commit()
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/users/profile")
async def some_url(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.id==user_info["id"]))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")
    
    session.execute(Delete(User).where(User.id==user_info["id"]))
    session.commit()
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.post("/users/profile/media")
async def set_board(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)], avatar: UploadFile) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.id==user_info["id"]))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")
    
    file_path = f"{settings.STATICFILES_DIR}/users/{user_info["id"]}/avatar/{avatar.filename}" 
    Media.save(avatar.file, path=file_path)
    
    instance.avatar = file_path
    session.add(instance)
    session.commit()    

    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.delete("/users/profile/media")
async def set_board(session: Annotated[Session, Depends(get_session)], user_info: Annotated[dict, Depends(get_user)]) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.id==user_info["id"]))
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found")
    
    file_path = f"{settings.STATICFILES_DIR}/users/{user_info["id"]}/avatar/" 
    Media.clean(path=file_path)
    
    instance.avatar = None
    session.add(instance)
    session.commit()
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)