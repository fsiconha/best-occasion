from __future__ import annotations

from functools import lru_cache

from qdrant_client import QdrantClient

from best_occasion.config.settings import Settings, get_settings
from best_occasion.embeddings.base import EmbeddingService
from best_occasion.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingService,
)
from best_occasion.matchmaking.engine import MatchmakingEngine
from best_occasion.registry.repositories.qdrant import QdrantVectorStore
from best_occasion.registry.repositories.vector_store import (
    VectorStoreRepository,
)
from best_occasion.services.recommendation import RecommendationService
from best_occasion.services.registry import RegistryService


@lru_cache
def get_cached_settings() -> Settings:
    """Expose cached settings instance for FastAPI dependency injection."""

    return get_settings()


@lru_cache
def get_qdrant_client() -> QdrantClient:
    """Return configured Qdrant client instance."""

    settings = get_cached_settings()
    if settings.vector_store_url:
        return QdrantClient(url=settings.vector_store_url)
    return QdrantClient(path=":memory:")


@lru_cache
def get_embedding_service() -> EmbeddingService:
    """Provide embedding service used across the application."""

    settings = get_cached_settings()
    return SentenceTransformerEmbeddingService(
        model_name=settings.embedding_model_name,
        instruction=settings.embedding_instruction,
    )


@lru_cache
def get_vector_store() -> VectorStoreRepository:
    """Instantiate the vector store repository backed by Qdrant."""

    return QdrantVectorStore(
        client=get_qdrant_client(),
        embedding=get_embedding_service(),
    )


@lru_cache
def get_registry_service() -> RegistryService:
    """Return registry service bound to the Qdrant repository."""

    return RegistryService(repository=get_vector_store())


@lru_cache
def get_matchmaking_engine() -> MatchmakingEngine:
    """Return matchmaking engine wired with the vector store repository."""

    return MatchmakingEngine(repository=get_vector_store())


@lru_cache
def get_recommendation_service() -> RecommendationService:
    """Return recommendation service that delegates to matchmaking."""

    return RecommendationService(engine=get_matchmaking_engine())
