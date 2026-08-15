from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL:str

    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int

    ADMIN_NAME:str
    ADMIN_PASSWORD:str

    RESEND_API:str
    FROM_EMAIL:str
    FRONTEND_URL:str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()