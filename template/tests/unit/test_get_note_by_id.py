from uuid import uuid4

import pytest

from app.application.use_cases.get_note_by_id import GetNoteById
from app.domain.entities.note import Note
from app.domain.exceptions.note_not_found import NoteNotFound
from tests.fakes.in_memory_note_repository import InMemoryNoteRepository


def _make_use_case(*, notes: list[Note] | None = None) -> GetNoteById:
    repository = InMemoryNoteRepository()
    for note in notes or []:
        repository.seed(note=note)
    return GetNoteById(note_repository=repository)


class TestGetNoteById:
    async def test_returns_note_when_repository_has_it(self) -> None:
        note = Note(note_id=uuid4(), title="Ship hexagonal template")
        use_case = _make_use_case(notes=[note])

        result = await use_case.execute(note_id=note.note_id)

        assert result == note

    async def test_raises_note_not_found_when_repository_is_empty(self) -> None:
        missing_note_id = uuid4()
        use_case = _make_use_case()

        with pytest.raises(NoteNotFound) as raised:
            await use_case.execute(note_id=missing_note_id)

        assert raised.value.note_id == missing_note_id
