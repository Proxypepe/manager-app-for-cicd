from unittest import mock
import pytest

from fastapi.testclient import TestClient

from src.repositories.room_repository import RoomRepository, RoomNotFoundError
from src.models.room import Room
from src.schemas.manager import CreateCredentials
from main import app


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def repository_mock():
    yield mock.Mock(spec=RoomRepository)


def test_get_list(client, repository_mock):
    repository_mock.get_all_rooms.return_value = [
        Room(id=1, owner_id='some_id', password='some_password', second_player_id=None, status='WAITING_FOR_OPPONENT',
             result='WAITING_FOR_RESULT', ),
        Room(id=2, owner_id='some_id', password='some_password', second_player_id=None, status='WAITING_FOR_OPPONENT',
             result='WAITING_FOR_RESULT', ),
    ]

    with app.container.room_repository.override(repository_mock):
        response = client.get('/api/v1/manager/list')

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {'id': 1, 'owner_id': 'some_id', 'password': 'some_password', 'second_player_id': None,
         'status': 'WAITING_FOR_OPPONENT', 'result': 'WAITING_FOR_RESULT'},
        {'id': 2, 'owner_id': 'some_id', 'password': 'some_password', 'second_player_id': None,
         'status': 'WAITING_FOR_OPPONENT', 'result': 'WAITING_FOR_RESULT'},
    ]


def test_create_room(client, repository_mock):
    repository_mock.create_room.return_value = \
        Room(id=1, owner_id='some_id', password='some_password',
             second_player_id=None,
             status='WAITING_FOR_OPPONENT', result='WAITING_FOR_RESULT'
             )
    request_data = CreateCredentials(
                owner_id='some_id',
                room_password='some_password'
            )
    with app.container.room_repository.override(repository_mock):
        response = client.post(
            '/api/v1/manager/create',
            data=request_data.json()
        )

    assert response.status_code == 201
    data = response.json()
    assert data == {'id': 1, 'owner_id': 'some_id', 'password': 'some_password', 'second_player_id': None,
                    'status': 'WAITING_FOR_OPPONENT', 'result': 'WAITING_FOR_RESULT'}
    repository_mock.create_room.assert_called_once_with(
        request_data
    )


def test_create_room_422(client, repository_mock):
    response = client.post(
        '/api/v1/manager/create'
    )
    assert response.status_code == 422


def test_delete_room(client, repository_mock):
    with app.container.room_repository.override(repository_mock):
        response = client.delete(
            '/api/v1/manager/delete',
            json={
                "room_id": 1,
                "player_id": ""

            })
    assert response.status_code == 204
    repository_mock.delete_room.assert_called_once_with(1)


def test_delete_room_404(client, repository_mock):
    repository_mock = mock.Mock(spec=RoomRepository)
    repository_mock.delete_room.side_effect = RoomNotFoundError(-1)

    with app.container.room_repository.override(repository_mock):
        response = client.delete(
            '/api/v1/manager/delete',
            json={
                "room_id": -1,
                "player_id": ""

            })
    assert response.status_code == 404
