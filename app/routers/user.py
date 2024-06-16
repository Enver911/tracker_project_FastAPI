from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from schemas.user import UserSchemaCreate, UserSchemaLogin, UserSchemaRead
from models.user import User

from backend.db_depends import get_session
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



router = APIRouter(tags=["User"])

@router.post("/user/registration") #add custom validations
async def user_registration(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaCreate) -> UserSchemaRead:
    user_schema.password = bcrypt_context.hash(user_schema.password)
    instance = User(**dict(user_schema))
    
    session.add(instance)
    session.commit()
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.post("/user/password_reset")
async def user_password_reset(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaLogin) -> UserSchemaRead: 
    pass


@router.post("/user/login") #add jwt auth
async def user_login(session: Annotated[Session, Depends(get_session)], user_schema: UserSchemaLogin) -> UserSchemaRead:
    instance = (session.scalar(select(User).where(User.username==user_schema.username)) or
                session.scalar(select(User).where(User.email==user_schema.username)))
    
    if not instance or not bcrypt_context.verify(user_schema.password, instance.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password")
    
    return UserSchemaRead.model_validate(instance, from_attributes=True)


@router.post("/user/logout")
async def user_logout(session: Annotated[Session, Depends(get_session)]) -> UserSchemaRead:
    pass