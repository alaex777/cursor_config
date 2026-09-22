from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.domain.entities.note import Note
from app.main import build_app
from tests.fakes.in_memory_note_repository import InMemoryNoteRepository


@pytest.fixture()
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    app = build_app(note_repository=InMemoryNoteRepository())
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


class TestHealthEndpoint:
    async def test_returns_ok_status(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGetNoteEndpoint:
    async def test_returns_note_when_it_exists(self) -> None:
        note = Note(note_id=uuid4(), title="Read hexagonal guide")
        repository = InMemoryNoteRepository()
        repository.seed(note=note)
        app = build_app(note_repository=repository)

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get(f"/notes/{note.note_id}")

        assert response.status_code == 200
        assert response.json() == {"note_id": str(note.note_id), "title": note.title}

    async def test_returns_404_when_note_is_missing(self, async_client: AsyncClient) -> None:
        response = await async_client.get(f"/notes/{uuid4()}")

        assert response.status_code == 404
