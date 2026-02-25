"""API v1 router aggregation."""
from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Import and register routers
from src.api.v1.auth import router as auth_router
from src.api.v1.categories import router as categories_router
from src.api.v1.ideas import router as ideas_router

api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(ideas_router)


@api_router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {
        "message": "InnovatEPAM Portal API v1",
        "endpoints": {
            "health": "/health",
            "docs": "/api/docs",
            "redoc": "/api/redoc",
        }
    }
