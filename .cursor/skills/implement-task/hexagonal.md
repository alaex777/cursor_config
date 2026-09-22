# Hexagonal Architecture Reference

## Layer map

```
src/app/
  domain/
    entities/        Pure Python dataclasses
    exceptions/      Domain errors (e.g. NoteNotFound)
    ports/           async typing.Protocol for outbound deps
  application/
    use_cases/       One class per use case; returns domain types
  infrastructure/
    persistence/     SQLAlchemy tables + repository adapters
  interfaces/
    api/schemas/     Pydantic v2 HTTP models
    api/             FastAPI routers — call use cases, map to schemas
  main.py            Composition root
tests/
  unit/              Use cases + in-process fake adapters
  fakes/             Fake ports shared by unit and HTTP tests
  integration/       HTTP via build_app + SQLAlchemy adapter
```

## Dependency rule

```
domain         no fastapi / sqlalchemy / pydantic / httpx
application    domain only (plus its own packages)
infrastructure implements domain ports
interfaces     application use cases + pydantic; no sqlalchemy
main.py        wires infrastructure → use cases → routers
```

`/health` is an inbound probe: Pydantic schema + router, no domain.

## Note example

### domain/ports/note_repository.py

```python
class NoteRepository(Protocol):
    async def get_note_by_id(self, *, note_id: UUID) -> Note | None: ...
    async def save_note(self, *, note: Note) -> None: ...
```

### application/use_cases/get_note_by_id.py

```python
class GetNoteById:
    def __init__(self, *, note_repository: NoteRepository) -> None:
        self._note_repository = note_repository

    async def execute(self, *, note_id: UUID) -> Note:
        found_note = await self._note_repository.get_note_by_id(note_id=note_id)
        if found_note is None:
            raise NoteNotFound(note_id=note_id)
        return found_note
```

### interfaces/api/schemas/note.py

```python
class NoteResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    note_id: UUID
    title: str
```

Routers receive use cases from `build_notes_router(*, get_note_by_id=...)`.
Do not use FastAPI `Depends` for ports or use cases.
