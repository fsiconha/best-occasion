from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    """Contract for services capable of producing embeddings."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the fixed vector size produced by the encoder."""

        raise NotImplementedError

    @abstractmethod
    def encode(self, payload: dict[str, str]) -> list[float]:
        """Encode the payload into a vector representation."""

        raise NotImplementedError
