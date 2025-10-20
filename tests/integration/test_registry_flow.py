"""Integration tests for registry flow via FastAPI routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from best_occasion.api.app import create_app
from best_occasion.api.dependencies import get_registry_service


@pytest.fixture()
def registry_test_client(mocked_registry_service) -> TestClient:
    app = create_app()

    def override_registry_service():
        return mocked_registry_service

    app.dependency_overrides[
        get_registry_service
    ] = override_registry_service
    return TestClient(app)


def test_post_occasions_registers_payload(
    registry_test_client: TestClient,
    mocked_qdrant_client,
    fake_occasion,
) -> None:
    response = registry_test_client.post(
        "/registry/occasions",
        json=[
            {
                "occasion_id": fake_occasion.occasion_id,
                "channel": fake_occasion.channel,
                "audience": fake_occasion.audience,
                "objective_weights": fake_occasion.objective_weights,
            }
        ],
    )

    assert response.status_code == 202

    points, _ = mocked_qdrant_client.scroll(
        collection_name="best_occasion_occasions",
        limit=10,
        with_payload=True,
    )
    stored_ids = {point.payload.get("occasion_id") for point in points}
    assert fake_occasion.occasion_id in stored_ids
