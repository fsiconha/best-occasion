from __future__ import annotations

from best_occasion.matchmaking.engine import MatchmakingEngine
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.models import RecommendationModel


class RecommendationService:
    """Expose high-level API to request recommendations - matchmaking engine."""

    def __init__(self, engine: MatchmakingEngine) -> None:
        self._engine = engine

    def recommend(self, occasion: Occasion) -> RecommendationModel | None:
        return self._engine.recommend(occasion)
