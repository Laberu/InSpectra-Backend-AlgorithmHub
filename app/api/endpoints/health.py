# health.py
from fastapi import APIRouter
import httpx
from app.core.config import ALGO_BACKEND_URL

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check for the API Hub and external services."""
    algo_status = "unreachable"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ALGO_BACKEND_URL}/health")
            if response.status_code == 200:
                algo_status = "healthy"
    except Exception:
        pass

    return {
        "status": "ok",
        "algorithm_backend": algo_status
    }
