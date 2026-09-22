from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NoteResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    note_id: UUID
    title: str = Field(min_length=1, max_length=255)
