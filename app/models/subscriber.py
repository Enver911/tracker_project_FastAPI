from backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String


class Subscriber(Base):
    __tablename__ = "subscriber"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(30), ForeignKey("user.id", ondelete="CASCADE"))
    card_id = Column(Integer, ForeignKey("card.id", ondelete="CASCADE"))
