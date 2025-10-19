from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from best_occasion.api.dependencies import get_recommendation_service
from best_occasion.api.schemas.base import (
    OccasionPayload,
    RecommendationResponse,
)
from best_occasion.registry.occasions import Occasion
from best_occasion.services.recommendation import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationResponse)
def recommend_model(
    payload: OccasionPayload,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    """Return the best model for the provided occasion payload."""

    occasion = Occasion(
        occasion_id=payload.occasion_id,
        channel=payload.channel,
        audience=payload.audience,
        objective_weights=payload.objective_weights,
    )
    recommended = service.recommend(occasion)
    if recommended is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommendation available for the given occasion",
        )
    return RecommendationResponse(
        model_id=recommended.model_id,
        name=recommended.name,
        provider=recommended.provider,
        capabilities=dict(recommended.capabilities),
    )
