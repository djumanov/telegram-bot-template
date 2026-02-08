"""
Application configuration using Pydantic Settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    # Bot Configuration
    bot_token: str = Field(..., description="Telegram bot token")
    bot_username: Optional[str] = Field(None, description="Bot username")
    
    # Admin Configuration
    admin_ids: str = Field(..., description="Comma-separated admin IDs")
    super_admin_id: int = Field(..., description="Super admin ID")
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///data/bot.db",
        description="Database connection URL"
    )
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_enabled: bool = Field(default=False)
    
    # Application Settings
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    default_language: str = Field(default="uz")
    available_languages: str = Field(default="uz,ru,en")
    
    # Features
    enable_analytics: bool = Field(default=True)
    enable_webhooks: bool = Field(default=False)
    webhook_url: Optional[str] = None
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_calls: int = Field(default=30)
    rate_limit_period: int = Field(default=60)
    
    # File Upload
    max_file_size: int = Field(default=10485760)  # 10MB
    allowed_file_types: str = Field(default=".pdf,.jpg,.png,.doc,.docx")
    
    # Business Settings
    support_chat_id: Optional[int] = None
    channel_id: Optional[str] = None
    payments_enabled: bool = Field(default=False)
    payment_provider_token: Optional[str] = None
    
    # Monitoring
    sentry_dsn: Optional[str] = None
    
    @field_validator('admin_ids')
    @classmethod
    def parse_admin_ids(cls, v: str) -> List[int]:
        """Parse comma-separated admin IDs"""
        return [int(id.strip()) for id in v.split(',') if id.strip()]
    
    @field_validator('available_languages')
    @classmethod
    def parse_languages(cls, v: str) -> List[str]:
        """Parse comma-separated languages"""
        return [lang.strip() for lang in v.split(',') if lang.strip()]
    
    @field_validator('allowed_file_types')
    @classmethod
    def parse_file_types(cls, v: str) -> List[str]:
        """Parse comma-separated file types"""
        return [ft.strip() for ft in v.split(',') if ft.strip()]
    
    @property
    def is_admin(self) -> callable:
        """Check if user is admin"""
        def check(user_id: int) -> bool:
            return user_id in self.admin_ids or user_id == self.super_admin_id
        return check
    
    @property
    def is_super_admin(self) -> callable:
        """Check if user is super admin"""
        def check(user_id: int) -> bool:
            return user_id == self.super_admin_id
        return check


# Global settings instance
settings = Settings()
