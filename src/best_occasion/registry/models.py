from dataclasses import dataclass


@dataclass(slots=True)
class RecommendationModel:
    """Describe a recommender model candidate managed by the registry."""

    model_id: str
    name: str
    journey: str
    objectives: tuple[str, ...]
