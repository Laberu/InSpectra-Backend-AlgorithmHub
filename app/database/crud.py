from sqlalchemy.orm import Session
from app.database.models import Project
from app.core.logger import logger

def save_project(db: Session, project: Project):
    """Save a new project to the database."""
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project_by_job_id(db: Session, job_id: str):
    """Fetch a project by job_id."""
    return db.query(Project).filter(Project.job_id == job_id).first()

def update_project_status(db: Session, job_id: str, status: str):
    """Update the status of a project."""
    project = db.query(Project).filter(Project.job_id == job_id).first()
    if not project:
        logger.warning(f"Tried to update status for missing project {job_id}")
        return None

    project.status = status
    db.commit()
    db.refresh(project)
    logger.info(f"Updated project {job_id} to status '{status}'")
    return project
