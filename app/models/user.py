from backend.db import Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    
    email = Column(String(30), primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(30))
    firstname = Column(String(30), nullable=True)
    lastname = Column(String(30), nullable=True)
    is_active = Column(Boolean, default=True)