from fastapi import FastAPI
from routers import board 
from routers import column


app = FastAPI()

app.include_router(board.router)
app.include_router(column.router)