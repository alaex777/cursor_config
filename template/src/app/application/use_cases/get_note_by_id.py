from uuid import UUID

from app.domain.entities.note import Note
from app.domain.exceptions.note_not_found import NoteNotFound
from app.domain.ports.note_repository import NoteRepository


class GetNoteById:
    def __init__(self, *, note_repository: NoteRepository) -> None:
        self._note_repository = note_repository

    async def execute(self, *, note_id: UUID) -> Note:
        found_note = await self._note_repository.get_note_by_id(note_id=note_id)
        if found_note is None:
            raise NoteNotFound(note_id=note_id)
        return found_note
