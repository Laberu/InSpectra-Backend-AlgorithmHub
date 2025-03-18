from sqlalchemy.orm import Session
from app.database.models import Project

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
    if project:
        project.status = status
        db.commit()
        db.refresh(project)
    return project