import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql-db/algorithm_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
ALGO_BACKEND_URL = os.getenv("ALGO_BACKEND_URL", "http://localhost:3000")
RESOURCE_BACKEND_URL = os.getenv("RESOURCE_BACKEND_URL", "http://localhost:4000")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 60))
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "https://auth.inspectra.site")
