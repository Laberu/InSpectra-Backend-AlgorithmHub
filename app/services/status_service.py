import httpx
from sqlalchemy.orm import Session
from app.database.models import Project
from app.database.crud import get_project_by_job_id, update_project_status
from app.core.config import ALGO_BACKEND_URL
from app.core.logger import logger

async def fetch_project_status(job_id: str):
    """Fetches the status of a project from Algorithm Backend."""
    url = f"{ALGO_BACKEND_URL}/api/status/{job_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Error fetching project status: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Error connecting to Algorithm Backend: {str(e)}")
        return None

async def fetch_all_project_statuses(db: Session):
    """Fetches and updates the status of all projects in the database."""
    projects = db.query(Project).all()
    results = []
    for project in projects:
        status_data = await fetch_project_status(project.job_id)
        if status_data:
            update_project_status(db, project.job_id, status_data.get("status"))
            results.append(status_data)
    return results

async def fetch_user_project_statuses(db: Session, user_id: str):
    """Fetches and updates the status of all projects related to a specific user."""
    projects = db.query(Project).filter(Project.user_id == user_id).all()
    results = []
    for project in projects:
        status_data = await fetch_project_status(project.job_id)
        if status_data:
            update_project_status(db, project.job_id, status_data.get("status"))
            results.append(status_data)
    return results
