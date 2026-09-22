from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.application.use_cases.get_note_by_id import GetNoteById
from app.domain.entities.note import Note
from app.domain.exceptions.note_not_found import NoteNotFound
from app.interfaces.api.schemas.note import NoteResponse


def build_notes_router(*, get_note_by_id: GetNoteById) -> APIRouter:
    router = APIRouter(tags=["notes"])

    @router.get("/notes/{note_id}", response_model=NoteResponse)
    async def get_note(note_id: UUID) -> NoteResponse:
        try:
            note = await get_note_by_id.execute(note_id=note_id)
        except NoteNotFound as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note {error.note_id} was not found",
            ) from error
        return _map_note_to_response(note=note)

    return router


def _map_note_to_response(*, note: Note) -> NoteResponse:
    return NoteResponse(note_id=note.note_id, title=note.title)
