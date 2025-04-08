import httpx
from app.core.config import RESOURCE_BACKEND_URL
from app.core.config import AUTH_SERVICE_URL
from app.core.logger import logger


async def send_to_resource_backend(
    user_id: str,
    job_id: str,
    zip_file_path: str,
    project_name: str,
    description: str,
    user_email: str
):
    """Uploads completed project output to Resource Backend and notifies user via email."""
    try:
        with open(zip_file_path, "rb") as zip_file:
            files = {"zipFile": (f"{job_id}.zip", zip_file, "application/zip")}
            data = {
                "userId": user_id,
                "jobId": job_id,
                "projectName": project_name,
                "description": description
            }
            async with httpx.AsyncClient() as client:
                # Step 1: Upload to Resource Backend
                response = await client.post(f"{RESOURCE_BACKEND_URL}/projects", data=data, files=files)
                response.raise_for_status()

                # Step 2: Notify via email
                notify_payload = {
                    "userid": user_id,
                    "projectName": project_name
                }
                notify_response = await client.post(f"{AUTH_SERVICE_URL}/auth/notify-project-completion", json=notify_payload)
                notify_response.raise_for_status()

                return {
                    "upload": response.json(),
                    "notification": notify_response.json()
                }

    except Exception as e:
        logger.error(f"Error sending project {job_id} to Resource Backend or sending email: {str(e)}")
        return None
