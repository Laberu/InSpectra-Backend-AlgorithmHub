import asyncio
import httpx
import os
from sqlalchemy.orm import Session
from app.database.db_session import SessionLocal
from app.database.models import Project
from app.database.crud import get_project_by_job_id, update_project_status
from app.services.algorithm_service import fetch_project_status, download_project_output
from app.services.redis_service import store_file_temporarily
from app.services.resource_service import send_to_resource_backend
from app.core.config import ALGO_BACKEND_URL, POLLING_INTERVAL
from app.core.logger import logger

async def check_and_process_jobs():
    """Checks all projects periodically and processes completed jobs."""
    while True:
        try:
            db: Session = SessionLocal()
            projects = db.query(Project).filter(Project.status != "stored").all()
            for project in projects:
                status_data = await fetch_project_status(project.job_id)
                if status_data and status_data.get("status") == "completed":
                    logger.info(f"Project {project.job_id} completed. Downloading output.")
                    await process_completed_project(db, project.job_id, project.user_id)
        except Exception as e:
            logger.error(f"Error checking job statuses: {str(e)}")
        finally:
            db.close()
        await asyncio.sleep(POLLING_INTERVAL)

async def process_completed_project(db: Session, job_id: str, user_id: str):
    """Downloads and sends completed job output to the Resource Backend."""
    try:
        project = get_project_by_job_id(db, job_id)
        if not project:
            logger.error(f"No project found with job_id {job_id}")
            return

        if project.status == "stored":
            logger.info(f"Project {job_id} already marked as stored. Skipping upload.")
            return

        logger.info(f"Downloading output for project {job_id} from Algorithm Backend.")
        zip_content = await download_project_output(job_id)
        if not zip_content:
            logger.error(f"Failed to download project {job_id}. No content received.")
            return

        temp_path = f"/tmp/{job_id}.zip"
        with open(temp_path, "wb") as f:
            f.write(zip_content)
        logger.info(f"File saved temporarily at {temp_path}")

        success = await send_to_resource_backend(
            user_id,
            job_id,
            temp_path,
            project.name,
            project.description
        )

        if success:
            update_project_status(db, job_id, "stored")
            logger.info(f"Project {job_id} output stored in Resource Backend.")
            os.remove(temp_path)  # Clean up temp file
        else:
            logger.error(f"Failed to store project {job_id} output in Resource Backend.")

    except Exception as e:
        logger.error(f"Failed to process completed project {job_id}: {str(e)}")


# Start job watcher in background
def start_job_watcher():
    loop = asyncio.get_event_loop()
    loop.create_task(check_and_process_jobs())