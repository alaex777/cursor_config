from typing import Protocol
from uuid import UUID

from app.domain.entities.note import Note


class NoteRepository(Protocol):
    async def get_note_by_id(self, *, note_id: UUID) -> Note | None: ...

    async def save_note(self, *, note: Note) -> None: ...
