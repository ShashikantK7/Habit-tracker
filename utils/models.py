from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String, unique=True, index=True)
    frequency = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class HabitTracking(Base):
    __tablename__ = "habit_tracking"

    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String, index=True)
    date = Column(Date)
    completed = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
