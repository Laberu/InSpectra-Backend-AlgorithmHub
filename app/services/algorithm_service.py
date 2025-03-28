import httpx
import logging
from io import BytesIO
from app.core.config import ALGO_BACKEND_URL

logger = logging.getLogger(__name__)

async def send_zip_to_algorithm(zip_data, filename: str):
    """Uploads a ZIP file to the Algorithm Backend.
    
    Supports both:
    - `zip_data` as a **file path** (string)
    - `zip_data` as **raw bytes** (bytes)
    """
    url = f"{ALGO_BACKEND_URL}/upload"
    timeout = httpx.Timeout(connect=60.0, read=300.0, write=300.0, pool=300.0)

    try:
        # Check if zip_data is a file path or raw bytes
        if isinstance(zip_data, str):
            if "\x00" in zip_data:
                raise ValueError("zip_data (file path) contains null bytes!")
            file_obj = open(zip_data, "rb")  # Open file from path
        elif isinstance(zip_data, bytes):
            file_obj = BytesIO(zip_data)  # Use BytesIO for in-memory file
        else:
            raise TypeError(f"zip_data must be str (file path) or bytes, got {type(zip_data)}")

        async with httpx.AsyncClient(timeout=timeout) as client:
            files = {"file": (filename, file_obj, "application/zip")}
            response = await client.post(url, files=files)
            response.raise_for_status()

            if response.headers.get("content-type") == "application/json":
                data = response.json()
                return {
                    "job_id": data.get("job_id"),
                    "status": data.get("grpc_status"),
                }
            else:
                logger.error("Unexpected response type from Algorithm Backend.")
                return {"error": "Invalid response format from algorithm"}

    except httpx.HTTPStatusError as e:
        logger.error(f"Algorithm Backend error: {e.response.status_code} - {e.response.text}")
        return {"error": "Algorithm Backend failed", "status_code": e.response.status_code}
    except Exception as e:
        logger.error(f"Error connecting to Algorithm Backend: {str(e)}", exc_info=True)
        return {"error": "Algorithm Backend connection failed"}
    finally:
        if 'file_obj' in locals() and not isinstance(zip_data, bytes):
            file_obj.close()  # Close file if it was opened from disk


async def fetch_project_status(job_id: str):
    """Fetches the status of a project from the Algorithm Backend."""
    url = f"{ALGO_BACKEND_URL}/status/{job_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching project status for {job_id}: {str(e)}", exc_info=True)
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
        logger.error(f"Error downloading project {job_id}: {str(e)}", exc_info=True)
        return None
