from .base import EmbeddingsProvider
from .local_sentence_transformers import LocalSentenceTransformerProvider
from .openai_provider import OpenAIEmbeddingsProvider
from config import settings


def get_provider() -> EmbeddingsProvider:

    if settings.embeddings_provider == "openai":
        return OpenAIEmbeddingsProvider()
    return LocalSentenceTransformerProvider()
