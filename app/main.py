from fastapi import FastAPI
from routers import board, column, card, user


app = FastAPI()

app.include_router(board.router)
app.include_router(column.router)
app.include_router(card.router)
app.include_router(user.router)
