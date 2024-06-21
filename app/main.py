from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from routers import board, column, card, user, follower, subscriber

import settings

from authentications.jwt_auth import get_user
from permissions.permissions import is_author_or_moderator

app = FastAPI()
app_v1 = FastAPI()
app.mount("/api/v1", app_v1)
app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATICFILES_DIR), name="static")

app_v1.include_router(board.router)
app_v1.include_router(column.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(card.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(user.router)
app_v1.include_router(follower.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(subscriber.router, dependencies=[Depends(is_author_or_moderator)])

@app.get("/")
def main_page(request: Request):
    print(app.root_path)
    return RedirectResponse(url="/api/v1/docs")