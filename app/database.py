from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Create the database engine using the URL from .env
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# SessionLocal is used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models (tables)
Base = declarative_base()

# Dependency for getting a database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
