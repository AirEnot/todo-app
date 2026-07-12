from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    allow_origins: list[str]


def get_settings():
    return Settings(
        DATABASE_URL= "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres",
        allow_origins=["http://localhost:3000"]
    )

