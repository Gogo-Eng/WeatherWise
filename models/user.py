#!/usr/bin/env python3
"""creating a SQLAlchemy model named User for a database table
"""

from sqlalchemy import create_engine, text, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    feedback = relationship("Feedback", back_populates="user")

class Feedback(Base):
    """User model"""

    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feedback_text = Column(Text, nullable=False)  # This is the feedback content
    session_id = Column(String(250), nullable=True)
    
    user = relationship("User", back_populates="feedback")