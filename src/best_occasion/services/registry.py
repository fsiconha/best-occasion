from __future__ import annotations

from typing import Iterable

from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.vector_store import (
    VectorStoreRepository,
)


class RegistryService:
    """Manage persistence of models and occasions via repositories."""

    def __init__(self, repository: VectorStoreRepository) -> None:
        self._repository = repository

    def register_models(self, models: Iterable[RecommendationModel]) -> None:
        self._repository.upsert_models(models)

    def register_occasions(self, occasions: Iterable[Occasion]) -> None:
        self._repository.upsert_occasions(occasions)
