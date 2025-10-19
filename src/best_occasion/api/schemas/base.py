"""Pydantic schemas used by the public API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OccasionPayload(BaseModel):
    """Input payload describing the occasion to be matched."""

    occasion_id: str = Field(
        ...,
        description="Unique identifier for the occasion",
    )
    channel: str = Field(
        ...,
        description="Channel or page where the model will run",
    )
    audience: str = Field(
        ...,
        description="Target audience description",
    )
    objective_weights: dict[str, float] = Field(
        default_factory=dict,
        description="Weights for business objectives to optimise",
    )


class RecommendationResponse(BaseModel):
    """Response payload containing the selected model."""

    model_id: str
    name: str
    provider: str
    capabilities: dict[str, float] = Field(default_factory=dict)


class ModelRegistrationPayload(BaseModel):
    """Payload for registering or updating recommendation models."""

    model_id: str
    name: str
    provider: str
    capabilities: dict[str, float] = Field(default_factory=dict)


class OccasionRegistrationPayload(BaseModel):
    """Payload for registering or updating occasions."""

    occasion_id: str
    channel: str
    audience: str
    objective_weights: dict[str, float] = Field(default_factory=dict)
