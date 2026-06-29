"""Common pytest fixtures for API tests."""

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture()
def client() -> TestClient:
    """Provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities_state() -> None:
    """Reset in-memory activities to keep tests independent."""
    original_state = deepcopy(activities)

    yield

    activities.clear()
    activities.update(original_state)
