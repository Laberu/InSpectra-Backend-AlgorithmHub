from fastapi import APIRouter
import httpx
from app.core.config import ALGO_BACKEND_URL, RESOURCE_BACKEND_URL
from app.core.logger import logger

router = APIRouter()

@router.get("/")
def health_check():
    """Health check for the API Hub, Algorithm Backend, and Resource Backend."""
    algo_status = "unreachable"
    resource_status = "unreachable"

    try:
        response = httpx.get(f"{ALGO_BACKEND_URL}/health")
        if response.status_code == 200:
            algo_status = "healthy"
    except Exception:
        pass
    
    try:
        response = httpx.get(f"{RESOURCE_BACKEND_URL}/health")
        if response.status_code == 200:
            resource_status = "healthy"
    except Exception:
        pass
    
    return {
        "status": "ok",
        "algorithm_backend": algo_status,
        "resource_backend": resource_status
    }