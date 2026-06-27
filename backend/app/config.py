from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional
import sys


class Settings(BaseSettings):
    # App
    APP_NAME: str = "LeadSync AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://leadpulse:leadpulse@localhost:5432/leadpulse_db"

    # Auth
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # AI
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Gorilla CRM
    GORILLA_API_URL: Optional[str] = None
    GORILLA_API_KEY: Optional[str] = None

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    @model_validator(mode="after")
    def validate_required_secrets(self) -> "Settings":
        errors = []

        if self.SECRET_KEY == "change-this-in-production":
            errors.append(
                "  ✗ SECRET_KEY is still the default placeholder — set a real random string."
            )

        if not self.ANTHROPIC_API_KEY:
            errors.append(
                "  ✗ ANTHROPIC_API_KEY is not set — AI qualification won't work."
            )

        if not self.DATABASE_URL:
            errors.append(
                "  ✗ DATABASE_URL is not set — the app cannot connect to the database."
            )

        if errors:
            print("\n🚨 LeadPulse startup failed — missing or invalid configuration:\n")
            for e in errors:
                print(e)
            print("\n  → Copy backend/.env.example to backend/.env and fill in your values.\n")
            sys.exit(1)

        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

