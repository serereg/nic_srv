from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Common:
    id = Column(Integer, primary_key=True)


class User(Common, Base):
    __tablename__ = "users"

    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(32), nullable=False)


class Session(Common, Base):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id"), nullable=False)
    token = Column(String(64), nullable=False, unique=True)


class Cooler(Common, Base):
    __tablename__ = "coolers"

    name = Column(String(8), unique=True, nullable=False)
    description = Column(Text, nullable=False, default=lambda: "")
