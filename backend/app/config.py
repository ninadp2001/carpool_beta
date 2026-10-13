from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://carpool:carpool@localhost:5432/carpool"
    jwt_secret: str = "change-me"
    jwt_expire_minutes: int = 60 * 24
    cors_origins: str = "http://localhost:5173"

    payment_mode: str = "mock"  # "mock" or "razorpay"
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""

    gst_rate: float = 0.18
    timezone: str = "Asia/Kolkata"  # used for "today", ride search dates and wash slots

    admin_email: str = "admin@example.com"
    admin_password: str = "Admin@12345"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


def local_tz() -> ZoneInfo:
    return ZoneInfo(get_settings().timezone)


def local_now() -> datetime:
    """Current time in the business timezone (naive, to compare with dates and slot times)."""
    return datetime.now(local_tz()).replace(tzinfo=None)
