from backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

PERMISSIONS = {"reader": "reader", "moderator": "moderator"}

class Follower(Base):
    __tablename__ = "follower"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(30), ForeignKey("user.id", ondelete="CASCADE"))
    board_id = Column(Integer, ForeignKey("board.id", ondelete="CASCADE"))
    
    permission = Column(String(30), default=PERMISSIONS["reader"])
    
    user = relationship("User")
    board = relationship("Board")