from __future__ import annotations

from functools import lru_cache

from best_occasion.config.settings import Settings, get_settings


@lru_cache
def get_cached_settings() -> Settings:
    """Expose cached settings instance for FastAPI dependency injection."""

    return get_settings()
