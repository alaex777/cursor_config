from uuid import UUID

from app.domain.entities.note import Note


class InMemoryNoteRepository:
    def __init__(self) -> None:
        self._notes: dict[UUID, Note] = {}

    def seed(self, *, note: Note) -> None:
        self._notes[note.note_id] = note

    async def get_note_by_id(self, *, note_id: UUID) -> Note | None:
        return self._notes.get(note_id)

    async def save_note(self, *, note: Note) -> None:
        self._notes[note.note_id] = note
