"""
Species Counterpoint Generator - FastAPI Application

Main application entry point for the counterpoint generation API.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import time
import logging
from dotenv import load_dotenv
from app.api.routes import router as api_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print("🎵 Species Counterpoint Generator starting up...")
    yield
    # Shutdown
    print("🎵 Species Counterpoint Generator shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Species Counterpoint Generator API",
    description="API for generating and evaluating species counterpoint music",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response

# Include API routes
app.include_router(api_router, prefix="/api", tags=["counterpoint"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "species-counterpoint-api",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Species Counterpoint Generator API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
