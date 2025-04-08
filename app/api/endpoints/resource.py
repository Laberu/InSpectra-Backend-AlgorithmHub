from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.core.config import RESOURCE_BACKEND_URL
from app.core.config import AUTH_SERVICE_URL
from app.core.logger import logger

router = APIRouter()

@router.post("/projects")
async def create_project(
    user_id: str = Form(...),
    project_name: str = Form(...),
    description: str = Form(...),
    zip_file: UploadFile = File(...)
):
    """Creates a new project in the Resource Backend."""
    try:
        files = {"zipFile": (zip_file.filename, await zip_file.read(), "application/zip")}
        data = {"userId": user_id, "projectName": project_name, "description": description}
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{RESOURCE_BACKEND_URL}/projects", data=data, files=files)
            response.raise_for_status()

            # Step 2: Notify via email
            notify_payload = {
                "userid": user_id,
                "projectName": project_name
            }
            notify_response = await client.post(f"{AUTH_SERVICE_URL}/auth/notify-project-completion", json=notify_payload)
            notify_response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Resource Backend error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=500, detail="Resource Backend request failed")

@router.get("/projects")
async def get_all_projects():
    """Fetch all projects from Resource Backend."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_BACKEND_URL}/projects")
        return response.json()

@router.get("/projects/{project_id}")
async def get_project_by_id(project_id: str):
    """Fetch a specific project by ID from Resource Backend."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_BACKEND_URL}/projects/{project_id}")
        return response.json()

@router.get("/projects/{project_id}/download")
async def download_project_zip(project_id: str):
    """Download project ZIP file from Resource Backend."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RESOURCE_BACKEND_URL}/projects/{project_id}/download")
        return response.json()

@router.put("/projects/{project_id}")
async def update_project(project_id: str, update_data: dict):
    """Update project details in Resource Backend."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{RESOURCE_BACKEND_URL}/projects/{project_id}", json=update_data)
        return response.json()

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project from Resource Backend."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RESOURCE_BACKEND_URL}/projects/{project_id}")
        return response.json()
