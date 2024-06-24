from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import logging

engine = create_engine("sqlite:///tracker.db", echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

#logger
logger = logging.getLogger('sqlalchemy.engine')

handler = logging.FileHandler('app.log', mode="w")
handler.setLevel(logging.INFO)

logger.addHandler(handler)


class Base(DeclarativeBase):
    def set(self, model_dump):
        for key, value in model_dump.items():
            setattr(self, key, value)