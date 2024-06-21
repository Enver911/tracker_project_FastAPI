from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from routers import board, column, card, user, follower, subscriber

import settings

from authentications.jwt_auth import get_user

app = FastAPI()
app_v1 = FastAPI()
app.mount("/api/v1", app_v1)
app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATICFILES_DIR), name="static")

app_v1.include_router(board.router, dependencies=[Depends(get_user)])
app_v1.include_router(column.router, dependencies=[Depends(get_user)])
app_v1.include_router(card.router, dependencies=[Depends(get_user)])
app_v1.include_router(user.router)
app_v1.include_router(follower.router, dependencies=[Depends(get_user)])
app_v1.include_router(subscriber.router, dependencies=[Depends(get_user)])


#add permission