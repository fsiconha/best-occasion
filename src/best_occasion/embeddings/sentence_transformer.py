from __future__ import annotations

from typing import Iterable

from sentence_transformers import SentenceTransformer

from best_occasion.embeddings.base import EmbeddingService


class SentenceTransformerEmbeddingService(EmbeddingService):
    """Produce embeddings using a compact E5 sentence-transformer model."""

    def __init__(
        self,
        model_name: str = "intfloat/e5-small-v2",
        *,
        instruction: str | None = None,
        normalize: bool = True,
    ) -> None:
        self._model_name = model_name
        self._instruction = instruction.strip() if instruction else ""
        self._normalize = normalize
        self._model = SentenceTransformer(model_name)
        self._dimension = int(self._model.get_sentence_embedding_dimension())

    @property
    def dimension(self) -> int:
        return self._dimension

    def encode(self, payload: dict[str, str]) -> list[float]:
        prompt = self._build_prompt(payload)
        embedding = self._model.encode(
            prompt,
            convert_to_numpy=True,
            normalize_embeddings=self._normalize,
        )
        if embedding.ndim != 1:
            msg = "SentenceTransformer returned an invalid embedding shape"
            raise ValueError(msg)
        return embedding.astype(float).tolist()

    def _build_prompt(self, payload: dict[str, str]) -> str:
        lines: list[str] = []
        for key, value in self._normalise_pairs(payload):
            safe_value = "" if value is None else str(value)
            lines.append(f"{key}: {safe_value}")
        body = "\n".join(lines)
        if not self._instruction:
            return body
        return f"{self._instruction}\n{body}" if body else self._instruction

    @staticmethod
    def _normalise_pairs(payload: dict[str, str]) -> Iterable[tuple[str, str]]:
        for key in sorted(payload):
            yield key, payload[key]
