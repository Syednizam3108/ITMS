from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import violations, officers, analytics, upload, detection, auth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Intelligent Traffic Management System API",
    description="Backend API for traffic violation management with MongoDB & YOLOv8",
    version="2.0.0"
)

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.abspath("app/static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(violations.router)
app.include_router(officers.router)
app.include_router(analytics.router)
app.include_router(analytics.stats_router)
app.include_router(upload.router)
app.include_router(detection.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Intelligent Traffic Management System API",
        "version": "1.0.0",
        "database": "MongoDB",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "MongoDB connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
