from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities_store)
    yield
    activities_store.clear()
    activities_store.update(original)
