from typing import Iterable

from .base import BaseRepository
from .room_dao import RoomDAO
from src.schemas.manager import Status, Result, CreateCredentials
from src.models.room import Room


class RoomRepository(BaseRepository, RoomDAO):
    async def get_room(self, pk: str) -> Room:
        with self.session_factory() as session:
            room = session.query(Room).filter(Room.id == pk).first()
            if not room:
                raise RoomNotFoundError(pk)
            return room

    async def get_all_rooms(self) -> Iterable[Room]:
        with self.session_factory() as session:
            return session.query(Room).all()

    async def create_room(self, credentials: CreateCredentials) -> Room:
        with self.session_factory() as session:
            room = Room(
                owner_id=credentials.owner_id,
                password=credentials.room_password,
                second_player_id=None,
                status=Status.WAITING_FOR_OPPONENT,
                result=Result.WAITING_FOR_RESULT,
            )
            session.add(room)
            session.commit()
            session.refresh(room)
            return room

    async def delete_room(self, room_id: int):
        with self.session_factory() as session:
            room = session.query(Room).filter(Room.id == room_id).first()
            if not room:
                raise RoomNotFoundError(room_id)
            session.delete(room)
            session.commit()


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class RoomNotFoundError(NotFoundError):

    entity_name: str = "Room"
