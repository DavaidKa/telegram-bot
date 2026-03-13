from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str
    ADMIN_IDS: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///bot.db"
    
    # Payment
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_SECRET: str = ""
    YOOMONEY_TOKEN: str = ""
    QIWI_SECRET_KEY: str = ""
    
    # AI Services
    OPENAI_API_KEY: str = ""
    STABILITY_API_KEY: str = ""
    AI_API_KEY: str = ""

    # Bot Settings
    VIP_PRICE_USD: float = 2.0
    REFERRAL_BONUS_DAYS: int = 3
    FREE_DAILY_LIMIT: int = 5
    WEBHOOK_URL: str = ""
    WEBHOOK_PATH: str = "/webhook"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def admin_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]


settings = Settings()

