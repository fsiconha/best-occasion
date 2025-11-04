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
        query_vector = self._retrieve_occasion_vector(occasion.occasion_id)
        if query_vector is None:
            return None
        results = self.client.query_points(
            collection_name=self.model_collection,
            query=query_vector,
            with_payload=True,
            limit=1,
        )
        if not results.points:
            return None
        record = results.points[0]
        return self._record_to_model(record)

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

    def _retrieve_occasion_vector(
        self,
        occasion_id: str,
    ) -> list[float] | None:
        self._ensure_collection(self.occasion_collection)
        normalized_id = self._normalize_id(occasion_id)
        records = self.client.retrieve(
            collection_name=self.occasion_collection,
            ids=[normalized_id],
            with_payload=False,
            with_vectors=True,
        )
        if not records:
            return None
        vector = records[0].vector
        if vector is None:
            return None
        if isinstance(vector, dict):
            vector = next(iter(vector.values()), None)
        if vector is None:
            return None
        return [float(value) for value in vector]

    def _record_to_model(
        self,
        record: qmodels.ScoredPoint,
    ) -> RecommendationModel:
        payload = record.payload or {}
        payload_objectives = payload.get("objectives") or []
        return RecommendationModel(
            model_id=str(payload.get("model_id", record.id)),
            name=str(payload.get("name", "")),
            journey=str(payload.get("journey", "")),
            objectives=tuple(
                str(obj)
                for obj in payload_objectives
                if isinstance(obj, str)
            ),
        )

    def _model_payload(self, model: RecommendationModel) -> dict[str, object]:
        return {
            "model_id": model.model_id,
            "name": model.name,
            "journey": model.journey,
            "objectives": list(model.objectives),
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
            "journey": model.journey,
            "objectives": json.dumps(
                sorted(model.objectives),
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
