from backend.db import Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.follower import Follower


class Board(Base):
    __tablename__ = "board" 
    
    id = Column(Integer, primary_key=True)
    author_email = Column(String(30), ForeignKey("user.email", ondelete="CASCADE"))
    
    title = Column(String(100), default="No name")
    description = Column(Text(1000), nullable=True)
    avatar = Column(String(100), nullable=True)
    background = Column(String(100), nullable=True)
    
    author = relationship("User", back_populates="boards")
    followers = relationship("User", secondary=Follower.__table__, back_populates="follows")
    columns = relationship("Column", back_populates="board")
    