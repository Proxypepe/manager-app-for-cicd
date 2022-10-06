from dependency_injector import containers, providers

from src.db.database import Database
from src.repositories.room_repository import RoomRepository
from src.services.room_service import RoomService
from src.core.config import Config


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["src.endpoints.manager"])

    config = Config()

    db = providers.Singleton(
        Database,
        db_url=f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

    room_repository = providers.Factory(
        RoomRepository,
        session_factory=db.provided.session,
    )

    room_service = providers.Factory(
        RoomService,
        room_repository=room_repository,
    )
