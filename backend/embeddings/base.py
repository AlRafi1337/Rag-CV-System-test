from abc import ABC, abstractmethod
from typing import List


class EmbeddingsProvider(ABC):

    @abstractmethod
    def embed(self, texts: List[str]) -> list[list[float]]:
        pass

    @abstractmethod
    def dim(self) -> int:
        pass
