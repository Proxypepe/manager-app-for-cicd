from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String

from .base import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(String(64), index=True)
    password = Column(String(255), nullable=True)
    second_player_id = Column(String(255), nullable=True)
    status = Column(String(255))
    result = Column(String(255))
