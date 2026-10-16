from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Battletech Chaos Campaign Manager API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Подключение к СУБД 
    DATABASE_URL: str = "sqlite+aiosqlite:///./campaign.db"
    
    # Безопасность и JWT
    SECRET_KEY: str = "SECRET_KEY_CHANGE_IN_PRODUCTION_MIN_32_CHARS_LONG"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 сутки

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()