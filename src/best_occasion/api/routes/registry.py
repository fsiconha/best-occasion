from __future__ import annotations

from fastapi import APIRouter, Body, Depends, status

from best_occasion.api.dependencies import get_registry_service
from best_occasion.api.schemas.base import (
    ModelRegistrationPayload,
    OccasionRegistrationPayload,
)
from best_occasion.registry.models import RecommendationModel
from best_occasion.registry.occasions import Occasion
from best_occasion.services.registry import RegistryService

router = APIRouter(prefix="/registry", tags=["registry"])


@router.post(
    "/models",
    status_code=status.HTTP_204_NO_CONTENT,
)
def register_model(
    models: list[ModelRegistrationPayload] = Body(...),
    service: RegistryService = Depends(get_registry_service),
) -> None:
    """Register or update recommendation models in the vector store."""

    domain_models = [
        RecommendationModel(
            model_id=item.model_id,
            name=item.name,
            provider=item.provider,
            capabilities=item.capabilities,
        )
        for item in models
    ]
    service.register_models(domain_models)


@router.post(
    "/occasions",
    status_code=status.HTTP_204_NO_CONTENT,
)
def register_occasion(
    occasions: list[OccasionRegistrationPayload] = Body(...),
    service: RegistryService = Depends(get_registry_service),
) -> None:
    """Register or update occasion embeddings in the vector store."""

    domain_occasions = [
        Occasion(
            occasion_id=item.occasion_id,
            channel=item.channel,
            audience=item.audience,
            objective_weights=item.objective_weights,
        )
        for item in occasions
    ]
    service.register_occasions(domain_occasions)
