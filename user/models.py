from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime
# from sqlalchemy import create_engine
from core.db import Base, engine


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    
Base.metadata.create_all(engine)