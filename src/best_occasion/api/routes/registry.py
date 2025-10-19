from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/registry", tags=["registry"])


@router.post("/models")
def register_model() -> None:
    """Placeholder endpoint for registering recommendation models."""

    raise NotImplementedError


@router.post("/occasions")
def register_occasion() -> None:
    """Placeholder endpoint for registering occasions."""

    raise NotImplementedError
