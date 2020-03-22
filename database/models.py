from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = declarative_base()


class Cooler(db):
    __tablename__ = "coolers"

    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=True, nullable=False)
    description = Column(Text, nullable=False, default=lambda: "")
