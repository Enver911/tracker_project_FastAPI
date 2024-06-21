from typing import Annotated
from fastapi import Depends, Request
from authentications.jwt_auth import get_user


async def tracker_permission(user_info: Annotated[dict, Depends(get_user)]) -> dict:
    return user_info