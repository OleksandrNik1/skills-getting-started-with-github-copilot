import sys
import os
import importlib

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import app
import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    import pytest
    # reload to ensure tests start with fresh in-memory data
    importlib.reload(app)
    return TestClient(app.app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Expect at least one activity and that structure contains participants
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    email = "pytest.user@mergington.edu"

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in app.activities[activity]["participants"]

    # Try signing up again should fail with 400
    repeat_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert repeat_resp.status_code == 400

    # Unregister
    delete_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert delete_resp.status_code == 200
    assert email not in app.activities[activity]["participants"]
