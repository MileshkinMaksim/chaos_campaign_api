from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Draconis Reach Campaign Manager API"
    VERSION: str = "6.0.0"
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str = "sqlite+aiosqlite:///./chaos_campaign.db"
    RAT_JSON_PATH: str = "app/db/data/factions_rat.json"

    model_config = ConfigDict(case_sensitive=True)


settings = Settings()