import uvicorn
from fastapi import FastAPI
from app.api.endpoints.health import router as health_router
from app.api.endpoints.projects import router as projects_router
from app.api.endpoints.status import router as status_router

app = FastAPI(title="Algorithm API Hub")

# Include API routes
app.include_router(health_router, prefix="/health")
app.include_router(projects_router, prefix="/projects")
app.include_router(status_router, prefix="/status")

@app.get("/")
def root():
    return {"message": "Algorithm API Hub is running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)