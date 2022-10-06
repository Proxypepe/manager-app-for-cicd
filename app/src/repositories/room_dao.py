from typing import Iterable
from abc import ABC, abstractmethod
from src.schemas.manager import CreateCredentials, Room


class RoomDAO(ABC):

    @abstractmethod
    async def get_room(self, pk: str) -> Room:
        pass

    @abstractmethod
    async def get_all_rooms(self) -> Iterable[Room]:
        pass

    @abstractmethod
    async def create_room(self, credentials: CreateCredentials) -> Room:
        pass

    @abstractmethod
    async def delete_room(self, room_id: int):
        pass
