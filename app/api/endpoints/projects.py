from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.services.project_service import create_project
from app.core.logger import logger

router = APIRouter()

@router.post("/create")
async def create_project_api(
    user_id: str = Form(...),  # Accept user_id from form-data
    name: str = Form(...),      # Accept name from form-data
    description: str = Form(...),  
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Handles project creation: uploads ZIP file and tracks job."""
    try:
        contents = await file.read()
        result = await create_project(db, user_id, name, description, contents, file.filename)
        return result
    except Exception as e:
        logger.error(f"Project creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Project creation failed")
