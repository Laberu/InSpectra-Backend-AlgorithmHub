import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql-db/algorithm_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
ALGO_BACKEND_URL = os.getenv("ALGO_BACKEND_URL", "http://localhost:3000")  # New
