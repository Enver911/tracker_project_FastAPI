from backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class Subscriber(Base):
    __tablename__ = "subscriber"
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String(30), ForeignKey("user.email", ondelete="CASCADE"))
    card_id = Column(Integer, ForeignKey("card.id", ondelete="CASCADE"))
