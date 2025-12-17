from sqlalchemy import (
    Column, Integer, String, SmallInteger,
    TIMESTAMP, Text, Date, ForeignKey, text
)
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fingerprint_id = Column(Integer, unique=True, nullable=False)
    access_level = Column(SmallInteger, default=1)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    journal = relationship("Journal", back_populates="user", uselist=False)

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    blood_type = Column(String(10), nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    photo_path = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="journal")

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    fingerprint_id = Column(Integer, nullable=False)
    granted = Column(SmallInteger, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User")
