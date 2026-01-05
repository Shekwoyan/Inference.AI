from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Patient, User, VitalSigns
from app.routes import patients, vitals

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare ERP API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(patients.router)
app.include_router(vitals.router)

@app.get("/")
def read_root():
    return {"message": "Healthcare ERP API is running!", "version": "1.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


