from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

#  Base declarative class
Base = declarative_base()

# Table `users`


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation with sessions and stats
    sessions = relationship("Sessions", back_populates="user")
    stats = relationship("Stats", back_populates="user", uselist=False)

# Table `sessions`


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    score = Column(Integer, default=0, nullable=False)
    exercises_completed = Column(Integer, default=0, nullable=False)
    successful_exercises = Column(Integer, default=0, nullable=False)

    # Relation avec l'utilisateur
    user = relationship("User", back_populates="sessions")

# Table `stats`


class Stats(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_sessions = Column(Integer, default=0, nullable=False)
    total_exercises = Column(Integer, default=0, nullable=False)
    average_score = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relation avec l'utilisateur
    user = relationship("User", back_populates="stats")
