from typing import Sequence

from fastapi import APIRouter, Depends, status, Response
from dependency_injector.wiring import inject, Provide

from src.di.containers import Container
from src.schemas.manager import Room as RoomSchema
from src.schemas.manager import JoinCredentials, DeleteCredentials, CreateCredentials
from src.repositories.room_dao import RoomDAO
from src.repositories.room_repository import RoomNotFoundError

manager_router = APIRouter()


@manager_router.get('/list', status_code=status.HTTP_200_OK, response_model=Sequence[RoomSchema])
@inject
async def get_room_list(
        room_service: RoomDAO = Depends(Provide[Container.room_service])
) -> Sequence[RoomSchema]:
    """
    Getting a list of available rooms
    """
    rooms = await room_service.get_all_rooms()
    return [RoomSchema.from_orm(room) for room in rooms]


@manager_router.post('/join', status_code=status.HTTP_200_OK)
@inject
async def join_room(
        credentials: JoinCredentials,
        room_service: RoomDAO = Depends(Provide[Container.room_service])
):
    """
    Password check
    """
    pass


@manager_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=RoomSchema)
@inject
async def create_room(
        credentials: CreateCredentials,
        room_service: RoomDAO = Depends(Provide[Container.room_service])
) -> RoomSchema:
    """
    Create a room
    """
    room = await room_service.create_room(credentials)
    return RoomSchema.from_orm(room)


@manager_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_room(
        credentials: DeleteCredentials,
        room_service: RoomDAO = Depends(Provide[Container.room_service])
):
    """
    Deleting a room
    """
    try:
        await room_service.delete_room(credentials.room_id)
    except RoomNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
