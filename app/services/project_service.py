from sqlalchemy.orm import Session
from app.services.algorithm_service import send_zip_to_algorithm
from app.database.models import Project
from app.database.crud import save_project
from app.core.logger import logger

async def create_project(
    db: Session,
    user_id: str,
    name: str,
    description: str,
    zip_file: bytes,
    filename: str
):
    """Handles the project creation process."""
    upload_result = await send_zip_to_algorithm(zip_file, filename)
    if "error" in upload_result:
        return {"error": "Failed to send job to algorithm"}

    job_id = upload_result.get("job_id")

    project = Project(
        user_id=user_id,
        job_id=job_id,
        status="queued",
        name=name,
        description=description
    )

    save_project(db, project)

    logger.info(f"Project created with job_id {job_id} for user {user_id}")

    return {
        "project_id": project.id,
        "user_id": user_id,
        "job_id": job_id,
        "status": "queued",
        "name": name,
        "description": description
    }





