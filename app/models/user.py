from backend.db import Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from models.follower import Follower
from models.subscriber import Subscriber

class User(Base):
    __tablename__ = "user"
    
    email = Column(String(30), primary_key=True)
    
    username = Column(String(30), unique=True)
    password = Column(String(30))
    avatar = Column(String(100), nullable=True)
    firstname = Column(String(30), nullable=True)
    lastname = Column(String(30), nullable=True)
    is_active = Column(Boolean, default=True)
    
    boards = relationship("Board", back_populates="author")
    follows = relationship("Board", secondary=Follower.__table__, back_populates="followers")
    subs = relationship("Card", secondary=Subscriber.__table__, back_populates="subscribers")