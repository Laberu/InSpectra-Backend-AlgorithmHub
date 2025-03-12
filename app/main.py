import uvicorn
from fastapi import FastAPI
from app.api.endpoints.health import router as health_router

app = FastAPI(title="Algorithm API Hub")

# Include API routes
app.include_router(health_router, prefix="/health")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
