"""Integration tests for the Qdrant-backed vector store and matchmaking."""

from __future__ import annotations

from qdrant_client import QdrantClient

from best_occasion.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingService,
)
from best_occasion.matchmaking.engine import MatchmakingEngine
from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.qdrant import QdrantVectorStore
from best_occasion.services.recommendation import RecommendationService


def test_recommendation_returns_best_model() -> None:
    embedding = SentenceTransformerEmbeddingService()
    repository = QdrantVectorStore(
        client=QdrantClient(path=":memory:"),
        embedding=embedding,
    )
    model = RecommendationModel(
        model_id="model-1",
        name="Baseline recommender",
        provider="in-house",
        capabilities={"ctr": 0.8, "conversion": 0.6},
    )
    repository.upsert_models([model])
    occasion = Occasion(
        occasion_id="occasion-1",
        channel="homepage",
        audience="new_users",
        objective_weights={"ctr": 1.0},
    )
    service = RecommendationService(engine=MatchmakingEngine(repository))

    recommendation = service.recommend(occasion)

    assert recommendation is not None
    assert recommendation.model_id == model.model_id
    assert recommendation.name == model.name
    assert recommendation.capabilities["ctr"] == model.capabilities["ctr"]
