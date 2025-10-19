from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    """Contract for services capable of producing embeddings."""

    @abstractmethod
    def encode(self, payload: dict[str, str]) -> list[float]:
        """Encode the payload into a vector representation."""

        raise NotImplementedError
