from __future__ import annotations

from fastapi import APIRouter, Depends

from best_occasion.api.dependencies import get_cached_settings
from best_occasion.api.schemas.base import (
    OccasionPayload,
    RecommendationResponse,
)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationResponse)
def recommend_model(
    payload: OccasionPayload,
    settings=Depends(get_cached_settings),
) -> RecommendationResponse:
    """Return the best model for the provided occasion payload."""

    del settings  # Placeholder until matchmaking is implemented
    return RecommendationResponse(
        model_id="demo",
        name="demo",
        provider="demo",
    )
