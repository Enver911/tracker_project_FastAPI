from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from routers import board, column, card, user, follower, subscriber

import sentry_sdk

import settings

from permissions.permissions import is_author_or_moderator

from debug_toolbar.middleware import DebugToolbarMiddleware

from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel

sentry_sdk.init(dsn="https://3dfd893c0f3c267b2e1c51c8bcc5b621@o4507482952761344.ingest.de.sentry.io/4507484177498192", traces_sample_rate=1.0, profiles_sample_rate=1.0)

app = FastAPI()
app_v1 = FastAPI()
#app_v1.add_middleware(DebugToolbarMiddleware, panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"])

app.mount("/api/v1", app_v1)
app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATICFILES_DIR), name="static")

app_v1.include_router(board.router)
app_v1.include_router(column.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(card.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(user.router)
app_v1.include_router(follower.router, dependencies=[Depends(is_author_or_moderator)])
app_v1.include_router(subscriber.router, dependencies=[Depends(is_author_or_moderator)])


@app.get("/")
async def main_page():
    return RedirectResponse(url="/api/v1/docs")