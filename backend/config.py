from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    database_url: str = "sqlite:///./shipment_intel.db"
    chroma_path: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    pkr_exchange_rate: float = 279.0
    demo_mode: bool = False
    aisstream_url: str = "wss://stream.aisstream.io/v0/stream"
    aisstream_key: str = ""
    shippo_api_key: str = ""
    hf_token: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
