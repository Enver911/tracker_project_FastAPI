from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.user import UserSchemaCreate, UserSchemaLogin, UserSchemaRead, JWT
from models.user import User

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, or_

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from jose import jwt, JWTError

import settings


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
router = APIRouter(tags=["User"])


@router.post("/users/registration") #add custom validations
async def user_registration(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaCreate) -> UserSchemaRead:
    
    if session.scalar(select(User).where(or_(User.username==user_schema.username, User.email==user_schema.email))): # if user exists 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    user_schema.password = bcrypt_context.hash(user_schema.password)
    instance = User(**dict(user_schema))
    
    session.add(instance)
    session.commit()
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.post("/users/password_reset")
async def user_password_reset(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaLogin) -> UserSchemaRead: 
    pass


@router.post("/users/logout")
async def user_logout(session: Annotated[Session, Depends(get_session)]) -> UserSchemaRead:
    pass


@router.post("/users/login")
async def user_login(session: Annotated[Session, Depends(get_session)], credentials: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JWT:
    
    instance = (session.scalar(select(User).where(User.username==credentials.username)) or
                session.scalar(select(User).where(User.email==credentials.username)))
    
    if not instance or not bcrypt_context.verify(credentials.password, instance.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username/email or password", headers={"WWW-Authenticate": "Bearer"})
    
    expires = (datetime.now() + settings.ACCESS_TOKEN_LIFETIME).timestamp()
    encode_dict = {"username": instance.username, "email": instance.email, "expires": expires}
    
    token = jwt.encode(claims=encode_dict, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return JWT(access_token=token)


async def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        user_info = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        if datetime.now() > datetime.fromtimestamp(float(user_info.get("expires"))):    
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token")
    
    return user_info


@router.get("/users/profile")
async def some_url(session: Annotated[Session, Depends(get_session)], user_info: dict = Depends(get_user)) -> UserSchemaRead:
    instance = session.scalar(select(User).where(User.username==user_info["username"]))
    return UserSchemaRead.model_validate(instance, from_attributes=True)