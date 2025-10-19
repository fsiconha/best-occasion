from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Protocol

from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion


class EmbeddingBackend(Protocol):
    """Defines the interface for embedding providers."""

    @property
    def dimension(self) -> int:
        """Return the dimensionality of produced vectors."""

        ...

    def encode(self, payload: dict[str, str]) -> list[float]:
        """Return embedding vector for given payload."""

        ...


class VectorStoreRepository(ABC):
    """Abstract repository for storing and querying embeddings."""

    @abstractmethod
    def upsert_models(self, models: Iterable[RecommendationModel]) -> None:
        """Persist or update recommendation models in the vector store."""

        raise NotImplementedError

    @abstractmethod
    def upsert_occasions(self, occasions: Iterable[Occasion]) -> None:
        """Persist or update occasions in the vector store."""

        raise NotImplementedError

    @abstractmethod
    def query_best_model(
        self,
        occasion: Occasion,
    ) -> RecommendationModel | None:
        """Return the best matching model for a given occasion."""

        raise NotImplementedError
