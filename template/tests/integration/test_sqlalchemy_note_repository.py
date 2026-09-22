from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.domain.entities.note import Note
from app.infrastructure.persistence.engine import create_engine, create_session_factory
from app.infrastructure.persistence.sqlalchemy_note_repository import SqlAlchemyNoteRepository
from app.infrastructure.persistence.tables import Base


@pytest.fixture()
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_engine(database_url="sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_session_factory(engine=engine)


class TestSqlAlchemyNoteRepository:
    async def test_returns_saved_note(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        repository = SqlAlchemyNoteRepository(session_factory=session_factory)
        note = Note(note_id=uuid4(), title="Persist via SQLAlchemy")

        await repository.save_note(note=note)
        found_note = await repository.get_note_by_id(note_id=note.note_id)

        assert found_note == note

    async def test_returns_none_when_note_is_missing(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        repository = SqlAlchemyNoteRepository(session_factory=session_factory)

        found_note = await repository.get_note_by_id(note_id=uuid4())

        assert found_note is None
