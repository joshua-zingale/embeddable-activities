import pytest
from fastapi.testclient import TestClient
from embeddable_activities.app import app


@pytest.fixture
def client():
    return TestClient(app)
