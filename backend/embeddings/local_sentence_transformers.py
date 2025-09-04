from .base import EmbeddingsProvider
from sentence_transformers import SentenceTransformer
from typing import List


class LocalSentenceTransformerProvider(EmbeddingsProvider):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model = SentenceTransformer(model_name)
        self._dim = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> list[list[float]]:
        return [emb.tolist() for emb in self._model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)]

    def dim(self) -> int:
        return self._dim
