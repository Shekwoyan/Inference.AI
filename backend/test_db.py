from app.database import engine, Base
from app.models import Patient, User

# Try to create tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Try to query
from app.database import SessionLocal
db = SessionLocal()
patients = db.query(Patient).all()
print(f"Found {len(patients)} patients")
db.close()