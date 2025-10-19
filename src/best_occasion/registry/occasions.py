from dataclasses import dataclass
from typing import Mapping


@dataclass(slots=True)
class Occasion:
    """Describe a context (page, audience, objective) that needs a model."""

    occasion_id: str
    channel: str
    audience: str
    objective_weights: Mapping[str, float]
