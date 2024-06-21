from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status

from jose import JWTError, jwt

import settings
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        user_info = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        
        if datetime.now() > datetime.fromtimestamp(float(user_info.get("expires"))):    
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token")
    
    return user_info