from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import patients, vitals, inference

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# Allow frontend or external apps to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (API endpoints)
app.include_router(patients.router, prefix=settings.API_V1_PREFIX)
app.include_router(vitals.router, prefix=settings.API_V1_PREFIX)
app.include_router(inference.router, prefix=settings.API_V1_PREFIX)

# Root endpoint


@app.get("/")
def root():
    return {"status": "ok", "message": "Inference.AI backend running"}
