from .base import EmbeddingsProvider
from typing import List
import os
import httpx


class OpenAIEmbeddingsProvider(EmbeddingsProvider):
    def __init__(self, model: str = "text-embedding-3-small", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for OpenAI provider")

    def embed(self, texts: List[str]) -> list[list[float]]:
        url = "https://api.openai.com/v1/embeddings"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        vectors: list[list[float]] = []
        with httpx.Client(timeout=60) as client:
            for i in range(0, len(texts), 1000):
                batch = texts[i:i+1000]
                resp = client.post(
                    url, json={"input": batch, "model": self.model}, headers=headers)
                resp.raise_for_status()
                data = resp.json()["data"]
                vectors.extend([d["embedding"] for d in data])
        return vectors

    def dim(self) -> int:
        # known dims for text-embedding-3-small = 1536; but avoid hardcoding
        return 1536
