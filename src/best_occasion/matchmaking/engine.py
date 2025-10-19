from __future__ import annotations

from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.vector_store import (
    VectorStoreRepository,
)
from best_occasion.registry.models import RecommendationModel


class MatchmakingEngine:
    """Coordinate repositories and heuristics to pick models."""

    def __init__(self, repository: VectorStoreRepository) -> None:
        self._repository = repository

    def recommend(self, occasion: Occasion) -> RecommendationModel | None:
        return self._repository.query_best_model(occasion)
