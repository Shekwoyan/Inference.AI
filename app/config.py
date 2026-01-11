import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    PROJECT_NAME: str = "Inference.AI Backend"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


# Create a settings instance
settings = Settings()
