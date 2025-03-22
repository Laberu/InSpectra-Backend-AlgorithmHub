import uvicorn
from fastapi import FastAPI
from app.api.endpoints.health import router as health_router
from app.api.endpoints.projects import router as projects_router
from app.api.endpoints.status import router as status_router
from app.api.endpoints.resource import router as resource_router
from app.services.job_watcher import start_job_watcher
from app.core.logger import logger
from app.database.db_session import engine
from app.database.models import Base

app = FastAPI(title="Algorithm API Hub")

# Include API routes
app.include_router(health_router, prefix="/health")
app.include_router(projects_router, prefix="/projects")
app.include_router(status_router, prefix="/status")
app.include_router(resource_router, prefix="/resource")

@app.get("/")
def root():
    return {"message": "Algorithm API Hub is running!"}

import time
from sqlalchemy.exc import OperationalError

@app.on_event("startup")
async def startup_event():
    print("🔧 Creating database tables if not exist...")
    for _ in range(10):  # Try for ~10s
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Tables checked/created.")
            break
        except OperationalError:
            print("⏳ Waiting for DB...")
            time.sleep(1)
    else:
        raise Exception("❌ Could not connect to DB after retries")

    start_job_watcher()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)