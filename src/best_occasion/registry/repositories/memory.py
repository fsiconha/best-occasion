from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.vector_store import (
    VectorStoreRepository,
)


@dataclass
class InMemoryVectorStore(VectorStoreRepository):
    """Simple in-memory storage to simulate vector search behaviour."""

    models: dict[str, RecommendationModel] = field(default_factory=dict)
    occasions: dict[str, Occasion] = field(default_factory=dict)

    def upsert_models(self, models: Iterable[RecommendationModel]) -> None:
        for model in models:
            self.models[model.model_id] = model

    def upsert_occasions(self, occasions: Iterable[Occasion]) -> None:
        for occasion in occasions:
            self.occasions[occasion.occasion_id] = occasion

    def query_best_model(
        self,
        occasion: Occasion,
    ) -> RecommendationModel | None:
        return next(iter(self.models.values()), None)
