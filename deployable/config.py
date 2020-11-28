from pydantic import Field
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Makes Services Deployable"
    admin_email: str = "jochen-deployable@wersdoerfer.de"
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()