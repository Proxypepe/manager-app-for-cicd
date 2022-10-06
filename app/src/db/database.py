from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, orm

from src.models.base import Base

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(
            db_url,
            # connect_args={"check_same_thread": False},
        )
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
