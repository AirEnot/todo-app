from dataclasses import dataclass
import os



@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    allow_origins: list[str]


def get_settings():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not set in environment variables")
    
    origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    origins_list = [origin.strip() for origin in origins_str.split(",")]
    
    return Settings(
        DATABASE_URL=database_url,
        allow_origins=origins_list
    )

