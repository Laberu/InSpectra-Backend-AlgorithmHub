from fastapi import FastAPI
from app.api.endpoints.health import router as health_router

app = FastAPI(title="Algorithm API Hub")

# Include API routes
app.include_router(health_router, prefix="/health")

# Root endpoint
def root():
    return {"message": "Algorithm API Hub is running!"}