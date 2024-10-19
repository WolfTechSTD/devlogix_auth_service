import os

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.adapter.persistence.db import new_session_maker
from app.config import DatabaseConfig


def test_new_session_maker(get_db_config: DatabaseConfig) -> None:
    session_maker = new_session_maker(get_db_config)
    assert isinstance(session_maker, async_sessionmaker)
