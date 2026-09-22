from fastapi import APIRouter

from app.interfaces.api.schemas.health import HealthResponse


def build_health_router() -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get("/health", response_model=HealthResponse)
    async def check_health() -> HealthResponse:
        return HealthResponse(status="ok")

    return router
