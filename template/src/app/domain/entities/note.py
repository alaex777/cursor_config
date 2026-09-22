from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Note:
    note_id: UUID
    title: str
