# src/app/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    KAFKA_BROKERS: str = "localhost:9092"
    TOPIC_INBOUND: str = "serve.vm.inbound"
    TOPIC_ONBOARDING: str = "serve.vm.onboarding"
    SERVICE_NAME: str = "vm-orchestrator"
    PORT: int = 8000
    # pydantic v2 way to load .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()