from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    anthropic_api_key: str = ""
    google_api_key: str = ""
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"
    database_url: str = "sqlite:///./shipment_intel.db"
    chroma_path: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    pkr_exchange_rate: float = 279.0
    demo_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
