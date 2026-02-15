from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:shree@localhost:5432/ride_pooling"
    REDIS_URL: str = "redis://localhost:6379"

settings = Settings()
