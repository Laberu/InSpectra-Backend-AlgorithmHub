from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.services.status_service import fetch_all_project_statuses, fetch_user_project_statuses
from app.core.logger import logger

router = APIRouter()

@router.get("/all")
async def get_all_project_statuses(db: Session = Depends(get_db)):
    """Fetches the status of all projects from Algorithm Backend."""
    try:
        result = await fetch_all_project_statuses(db)
        return result
    except Exception as e:
        logger.error(f"Error fetching all project statuses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching all project statuses")

@router.get("/user/{user_id}")
async def get_user_project_statuses(user_id: str, db: Session = Depends(get_db)):
    """Fetches the status of all projects related to a specific user."""
    try:
        result = await fetch_user_project_statuses(db, user_id)
        return result
    except Exception as e:
        logger.error(f"Error fetching user project statuses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching user project statuses")