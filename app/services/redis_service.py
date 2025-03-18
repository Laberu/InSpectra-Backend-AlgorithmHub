import redis
from app.core.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL)

def store_file_temporarily(job_id: str, file_content: bytes):
    """Stores file temporarily in Redis."""
    redis_client.setex(job_id, 3600, file_content)  # Expires in 1 hour
    return job_id
