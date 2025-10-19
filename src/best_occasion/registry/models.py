from dataclasses import dataclass
from typing import Mapping


@dataclass(slots=True)
class RecommendationModel:
    """Describe a recommender model candidate managed by the registry."""

    model_id: str
    name: str
    provider: str
    capabilities: Mapping[str, float]
