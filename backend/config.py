from pydantic import BaseModel, Field
import os


class Settings(BaseModel):

    database_url: str = Field(default_factory=lambda: os.getenv(
        "DATABASE_URL", "postgresql+psycopg://rag:ragpass@db:5432/ragcv"
    ))  # Ensure default and env both use ragcv
    vector_dim: int = int(os.getenv("VECTOR_DIM", "384"))
    embeddings_provider: str = os.getenv("EMBEDDINGS_PROVIDER", "local")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    file_storage_root: str = os.getenv("FILE_STORAGE_ROOT", "/uploads")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    # email
    imap_host: str = os.getenv("IMAP_HOST", "")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))
    imap_username: str = os.getenv("IMAP_USERNAME", "")
    imap_password: str = os.getenv("IMAP_PASSWORD", "")
    imap_folder: str = os.getenv("IMAP_FOLDER", "INBOX")
    imap_poll_seconds: int = int(os.getenv("IMAP_POLL_SECONDS", "60"))
    # server
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    # providers
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


settings = Settings()
