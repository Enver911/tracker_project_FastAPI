from fastapi import FastAPI, Depends
from routers import board, column, card, user, follower

from authentications.jwt_auth import get_user

app = FastAPI()

app.include_router(board.router, dependencies=[Depends(get_user)])
app.include_router(column.router, dependencies=[Depends(get_user)])
app.include_router(card.router, dependencies=[Depends(get_user)])
app.include_router(user.router)
app.include_router(follower.router, dependencies=[Depends(get_user)])


#add followers, subscribers api
#add nested pydantic models for followers, subscribers
#add permission
#add static files support
#change api links and set versioning
#deploy