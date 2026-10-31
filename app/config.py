from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_receptionist.db"
    secret_key: str = "change-this-to-a-long-random-string-in-production"
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # AI settings are primarily configured from the Admin panel (database).
    # These are only fallbacks if nothing is saved in Admin → Settings.
    ai_base_url: str = ""
    ai_api_key: Optional[str] = None
    ai_model: str = ""

    business_name: str = "My Business"
    business_timezone: str = "Asia/Dhaka"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
