"""Deterministic hash-based embedding service for local development."""

from __future__ import annotations

import hashlib
from typing import Iterable

from best_occasion.embeddings.base import EmbeddingService


class HashEmbeddingService(EmbeddingService):
    """Generate pseudo-random vectors derived from the input payload."""

    def __init__(self, dimension: int = 64) -> None:
        if dimension <= 0:
            msg = "Embedding dimension must be positive"
            raise ValueError(msg)
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def encode(self, payload: dict[str, str]) -> list[float]:
        message = "|".join(
            f"{key}:{value}" for key, value in sorted(payload.items())
        )
        digest = hashlib.sha256(message.encode("utf-8")).digest()
        raw_values = self._expand_digest(digest)
        return raw_values[: self._dimension]

    def _expand_digest(self, digest: bytes) -> list[float]:
        values: list[float] = []
        for chunk in self._chunks(digest, 4):
            integer = int.from_bytes(chunk, byteorder="big", signed=False)
            normalised = (integer % 2000) / 1000.0 - 1.0
            values.append(normalised)
            if len(values) >= self._dimension:
                break
        if not values:
            values.append(0.0)
        while len(values) < self._dimension:
            deficit = self._dimension - len(values)
            values.extend(values[:deficit])
        return values[: self._dimension]

    @staticmethod
    def _chunks(data: bytes, size: int) -> Iterable[bytes]:
        for start in range(0, len(data), size):
            yield data[start:start + size]
