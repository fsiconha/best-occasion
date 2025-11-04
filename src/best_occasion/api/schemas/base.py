"""Pydantic schemas used by the public API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OccasionPayload(BaseModel):
    """Input payload containing the target occasion identifier."""

    occasion_id: str = Field(
        ...,
        description="Identifier of the stored occasion to evaluate",
    )


class RecommendationResponse(BaseModel):
    """Response payload containing the selected model."""

    model_id: str
    name: str
    journey: str = Field(
        ...,
        description=(
            "CRM journey where the model applies (e.g. 'recompra')."
        ),
    )
    objectives: list[str] = Field(
        default_factory=list,
        description=(
            "List of objectives the model optimises (e.g. ['ctr'])."
        ),
    )


class ModelRegistrationPayload(BaseModel):
    """Payload for registering or updating recommendation models."""

    model_id: str
    name: str
    journey: str = Field(
        ...,
        description=(
            "CRM journey tag for the model (e.g. 'fidelizacao')."
        ),
    )
    objectives: list[str] = Field(
        default_factory=list,
        description=(
            "Objectives supported by the model as a list of strings."
        ),
    )


class OccasionRegistrationPayload(BaseModel):
    """Payload for registering or updating occasions."""

    occasion_id: str
    channel: str
    audience: str
    objective_weights: dict[str, float] = Field(default_factory=dict)
