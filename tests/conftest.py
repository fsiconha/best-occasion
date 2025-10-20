from __future__ import annotations

from collections.abc import Iterator

import pytest
from qdrant_client import QdrantClient

from best_occasion.embeddings.base import EmbeddingService
from best_occasion.registry.occasions import Occasion
from best_occasion.registry.repositories.qdrant import QdrantVectorStore
from best_occasion.services.registry import RegistryService


class FakeEmbeddingService(EmbeddingService):
    """Deterministic embedding generator for unit and integration tests."""

    def __init__(self, dimension: int = 6) -> None:
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def encode(self, payload: dict[str, str]) -> list[float]:
        values: list[float] = []
        for key in sorted(payload):
            raw_value = payload.get(key, "")
            safe_value = "" if raw_value is None else str(raw_value)
            values.append(float(len(safe_value)))
        while len(values) < self._dimension:
            values.append(0.0)
        return values[: self._dimension]


@pytest.fixture()
def fake_embedding_service() -> EmbeddingService:
    return FakeEmbeddingService()


@pytest.fixture()
def mocked_qdrant_client() -> Iterator[QdrantClient]:
    client = QdrantClient(path=":memory:")
    yield client


@pytest.fixture()
def mocked_vector_store(
    mocked_qdrant_client: QdrantClient,
    fake_embedding_service: EmbeddingService,
) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=mocked_qdrant_client,
        embedding=fake_embedding_service,
    )


@pytest.fixture()
def mocked_registry_service(
    mocked_vector_store: QdrantVectorStore,
) -> RegistryService:
    return RegistryService(repository=mocked_vector_store)


@pytest.fixture()
def fake_occasion() -> Occasion:
    return Occasion(
        occasion_id="occasion-test",
        channel="test-channel",
        audience="test-audience",
        objective_weights={"ctr": 1.0, "conversion": 0.5},
    )


@pytest.fixture()
def registered_fake_occasion(
    mocked_registry_service: RegistryService,
    fake_occasion: Occasion,
) -> Occasion:
    mocked_registry_service.register_occasions([fake_occasion])
    return fake_occasion
