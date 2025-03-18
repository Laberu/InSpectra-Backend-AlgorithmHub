import httpx
from app.core.config import RESOURCE_BACKEND_URL
from app.core.logger import logger

async def send_to_resource_backend(user_id: str, job_id: str, zip_file_path: str):
    """Uploads completed project output to Resource Backend."""
    try:
        with open(zip_file_path, "rb") as zip_file:
            files = {"zipFile": (f"{job_id}.zip", zip_file, "application/zip")}
            data = {
                "userId": user_id,
                "projectName": f"Processed-{job_id}",
                "description": "Auto-processed result"
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{RESOURCE_BACKEND_URL}/projects", data=data, files=files)
                response.raise_for_status()
                return response.json()
    except Exception as e:
        logger.error(f"Error sending project {job_id} to Resource Backend: {str(e)}")
        return None
