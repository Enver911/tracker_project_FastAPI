from backend.db import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column as Col
from sqlalchemy.orm import relationship


class Column(Base):
    __tablename__ = "column" 
    
    id = Col(Integer, primary_key=True)
    board_id = Col(Integer, ForeignKey("board.id", ondelete="CASCADE"))
    
    title = Col(String(100), default="No name")
    
    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column")