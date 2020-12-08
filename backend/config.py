from pydantic import Field
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Makes Services Deployable"
    admin_email: str = "jochen-deployable@wersdoerfer.de"
    password_hash_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")

    class Config:
        env_file = ".env"


settings = Settings()