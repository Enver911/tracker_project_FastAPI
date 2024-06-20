from backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class Follower(Base):
    PERMISSIONS = [("reader", "READER"), ("moderator", "MODERATOR")]
    
    __tablename__ = "follower"
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String(30), ForeignKey("user.email", ondelete="CASCADE"))
    board_id = Column(Integer, ForeignKey("board.id", ondelete="CASCADE"))
    
    permission = Column(ChoiceType(PERMISSIONS), default=PERMISSIONS[0][0])