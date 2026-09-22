from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.entities.note import Note
from app.infrastructure.persistence.tables import NoteTable


class SqlAlchemyNoteRepository:
    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def get_note_by_id(self, *, note_id: UUID) -> Note | None:
        async with self._session_factory() as session:
            statement = select(NoteTable).where(NoteTable.note_id == note_id)
            result = await session.execute(statement)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return Note(note_id=row.note_id, title=row.title)

    async def save_note(self, *, note: Note) -> None:
        async with self._session_factory() as session, session.begin():
            session.add(NoteTable(note_id=note.note_id, title=note.title))
