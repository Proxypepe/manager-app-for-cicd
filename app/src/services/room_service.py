from typing import Iterable

from src.repositories.room_repository import RoomRepository
from src.models.room import Room
from src.schemas.manager import Status, Result, CreateCredentials


class RoomService:

    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    async def get_room(self, pk: str) -> Room:
        return await self.room_repository.get_room(pk)

    async def get_all_rooms(self) -> Iterable[Room]:
        return await self.room_repository.get_all_rooms()

    async def create_room(self, credentials: CreateCredentials) -> Room:
        return await self.room_repository.create_room(credentials)

    async def delete_room(self, room_id: int):
        await self.room_repository.delete_room(room_id)

