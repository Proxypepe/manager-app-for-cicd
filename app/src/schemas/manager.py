import typing
import enum

from pydantic import BaseModel


class Status(str, enum.Enum):
    WAITING_FOR_OPPONENT = 'WAITING_FOR_OPPONENT'
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'


class Result(str, enum.Enum):
    FIRST_PLAYER_WIN = 'FIRST_PLAYER_WIN'
    SECOND_PLAYER_WIN = 'SECOND_PLAYER_WIN'
    DRAW = 'DRAW'
    WAITING_FOR_RESULT = 'WAITING_FOR_RESULT'


class Room(BaseModel):
    id: int
    owner_id: str
    password: typing.Optional[str]
    second_player_id: typing.Optional[str]
    status: Status
    result: Result

    class Config:
        use_enum_values = True
        orm_mode = True


class Credentials(BaseModel):
    room_id: int
    player_id: str


class JoinCredentials(Credentials):
    room_password: str


class DeleteCredentials(Credentials):
    ...


class CreateCredentials(BaseModel):
    owner_id: str
    room_password: typing.Optional[str]
