from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Iterable

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.vector_store import (
    EmbeddingBackend,
    VectorStoreRepository,
)


@dataclass
class QdrantVectorStore(VectorStoreRepository):
    """Persist and query model/occasion embeddings inside Qdrant."""

    client: QdrantClient
    embedding: EmbeddingBackend
    model_collection: str = "best_occasion_models"
    occasion_collection: str = "best_occasion_occasions"
    _initialized_collections: set[str] = field(default_factory=set)

    def upsert_models(self, models: Iterable[RecommendationModel]) -> None:
        self._ensure_collection(self.model_collection)
        points = [self._model_to_point(model) for model in models]
        if not points:
            return
        self.client.upsert(
            collection_name=self.model_collection,
            points=points,
        )

    def upsert_occasions(self, occasions: Iterable[Occasion]) -> None:
        self._ensure_collection(self.occasion_collection)
        points = [self._occasion_to_point(occasion) for occasion in occasions]
        if not points:
            return
        self.client.upsert(
            collection_name=self.occasion_collection,
            points=points,
        )

    def query_best_model(
        self,
        occasion: Occasion,
    ) -> RecommendationModel | None:
        self._ensure_collection(self.model_collection)
        query_vector = self.embedding.encode(
            self._occasion_embedding_payload(occasion)
        )
        results = self.client.search(
            collection_name=self.model_collection,
            query_vector=query_vector,
            limit=1,
            with_payload=True,
        )
        if not results:
            return None
        record = results[0]
        payload = record.payload or {}
        payload_capabilities = payload.get("capabilities") or {}
        return RecommendationModel(
            model_id=str(payload.get("model_id", record.id)),
            name=str(payload.get("name", "")),
            provider=str(payload.get("provider", "")),
            capabilities={
                key: float(value)
                for key, value in payload_capabilities.items()
            },
        )

    def _model_to_point(
        self,
        model: RecommendationModel,
    ) -> qmodels.PointStruct:
        payload = self._model_payload(model)
        vector = self.embedding.encode(self._model_embedding_payload(model))
        return qmodels.PointStruct(
            id=self._normalize_id(model.model_id),
            vector=vector,
            payload=payload,
        )

    def _occasion_to_point(self, occasion: Occasion) -> qmodels.PointStruct:
        payload = self._occasion_payload(occasion)
        vector = self.embedding.encode(
            self._occasion_embedding_payload(occasion)
        )
        return qmodels.PointStruct(
            id=self._normalize_id(occasion.occasion_id),
            vector=vector,
            payload=payload,
        )

    def _model_payload(self, model: RecommendationModel) -> dict[str, object]:
        return {
            "model_id": model.model_id,
            "name": model.name,
            "provider": model.provider,
            "capabilities": dict(model.capabilities),
        }

    def _occasion_payload(self, occasion: Occasion) -> dict[str, object]:
        return {
            "occasion_id": occasion.occasion_id,
            "channel": occasion.channel,
            "audience": occasion.audience,
            "objective_weights": dict(occasion.objective_weights),
        }

    def _model_embedding_payload(
        self,
        model: RecommendationModel,
    ) -> dict[str, str]:
        return {
            "model_id": model.model_id,
            "name": model.name,
            "provider": model.provider,
            "capabilities": json.dumps(
                dict(model.capabilities),
                sort_keys=True,
            ),
        }

    def _occasion_embedding_payload(
        self,
        occasion: Occasion,
    ) -> dict[str, str]:
        return {
            "occasion_id": occasion.occasion_id,
            "channel": occasion.channel,
            "audience": occasion.audience,
            "objective_weights": json.dumps(
                dict(occasion.objective_weights),
                sort_keys=True,
            ),
        }

    def _ensure_collection(self, name: str) -> None:
        if name in self._initialized_collections:
            return
        exists = False
        try:
            exists = self.client.collection_exists(name)
        except (UnexpectedResponse, ValueError):
            exists = False
        if not exists:
            self.client.create_collection(
                collection_name=name,
                vectors_config=qmodels.VectorParams(
                    size=self.embedding.dimension,
                    distance=qmodels.Distance.COSINE,
                ),
            )
        self._initialized_collections.add(name)

    @staticmethod
    def _normalize_id(raw_id: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"best-occasion:{raw_id}"))
