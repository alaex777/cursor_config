from uuid import UUID


class NoteNotFound(Exception):
    def __init__(self, *, note_id: UUID) -> None:
        self.note_id = note_id
        super().__init__(f"Note {note_id} was not found")
