import httpx
from app.core.config import ALGO_BACKEND_URL
from app.core.logger import logger

async def send_zip_to_algorithm(zip_file: bytes, filename: str):
    """Uploads a ZIP file to the Algorithm Backend."""
    url = f"{ALGO_BACKEND_URL}/upload"
    files = {"file": (filename, zip_file, "application/zip")}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            return {"job_id": data.get("job_id"), "status": data.get("grpc_status")}
    except httpx.HTTPStatusError as e:
        logger.error(f"Algorithm Backend error: {e.response.status_code} - {e.response.text}")
        return {"error": "Algorithm Backend failed", "status_code": e.response.status_code}
    except Exception as e:
        logger.error(f"Error connecting to Algorithm Backend: {str(e)}")
        return {"error": "Algorithm Backend connection failed"}
    
async def fetch_project_status(job_id: str):
    """Fetches the status of a project from the Algorithm Backend."""
    url = f"{ALGO_BACKEND_URL}/status/{job_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching project status for {job_id}: {str(e)}")
        return None

async def download_project_output(job_id: str):
    """Downloads project output from Algorithm Backend."""
    url = f"{ALGO_BACKEND_URL}/download/{job_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
    except Exception as e:
        logger.error(f"Error downloading project {job_id}: {str(e)}")
        return None
