from pathlib import Path

from pydantic import Field
from pydantic import BaseSettings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    app_name: str = "Makes Services Deployable"
    admin_email: str = "jochen-deployable@wersdoerfer.de"
    password_hash_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    test: bool = Field(default=False, env="TEST")
    origins: list[str] = [
        "http://localhost",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ROOT_DIR / ".env"


class TestSettings(Settings):
    database_url: str = Field(..., env="TEST_DATABASE_URL")


settings = Settings()
if settings.test:
    settings = TestSettings()
