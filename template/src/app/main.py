from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.use_cases.get_note_by_id import GetNoteById
from app.domain.ports.note_repository import NoteRepository
from app.infrastructure.persistence.engine import create_engine, create_session_factory
from app.infrastructure.persistence.sqlalchemy_note_repository import SqlAlchemyNoteRepository
from app.infrastructure.persistence.tables import Base
from app.interfaces.api.health_router import build_health_router
from app.interfaces.api.notes_router import build_notes_router

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


def build_app(
    *,
    database_url: str = DEFAULT_DATABASE_URL,
    note_repository: NoteRepository | None = None,
) -> FastAPI:
    """Composition root: wire infrastructure → use cases → interfaces."""
    engine = create_engine(database_url=database_url)
    resolved_note_repository = note_repository or SqlAlchemyNoteRepository(
        session_factory=create_session_factory(engine=engine),
    )
    get_note_by_id = GetNoteById(note_repository=resolved_note_repository)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app = FastAPI(title="Service", version="0.1.0", lifespan=lifespan)
    app.include_router(build_health_router())
    app.include_router(build_notes_router(get_note_by_id=get_note_by_id))
    return app


app = build_app()
