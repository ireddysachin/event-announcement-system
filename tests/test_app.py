
import os
import sys
import sqlite3
import tempfile
from pathlib import Path

# Make the app folder available for importing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

# Give the tests their own database
TEST_DB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
TEST_DB.close()
os.environ["EVENTS_DATABASE_PATH"] = TEST_DB.name

from database import initialize_database, get_connection
from app import app

initialize_database()


def setup_function():
    # Clear only the isolated test database
    with sqlite3.connect(TEST_DB.name) as connection:
        connection.execute("DELETE FROM events")
        connection.execute("DELETE FROM subscribers")
        connection.commit()




def test_homepage_loads():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Event Announcement System" in response.data


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_subscribe_successfully():
    client = app.test_client()

    response = client.post(
        "/subscribe",
        json={"email": "sachin@example.com"}
    )

    assert response.status_code == 201
    assert response.json["success"] is True

    with get_connection() as connection:
        subscriber = connection.execute(
            "SELECT email FROM subscribers WHERE email = ?",
            ("sachin@example.com",)
        ).fetchone()

    assert subscriber is not None
    assert subscriber["email"] == "sachin@example.com"


def test_duplicate_subscription():
    client = app.test_client()

    # First subscription should succeed.
    first_response = client.post(
        "/subscribe",
        json={"email": "sachin@example.com"}
    )

    assert first_response.status_code == 201

    # The same email should not be accepted twice.
    second_response = client.post(
        "/subscribe",
        json={"email": "sachin@example.com"}
    )

    assert second_response.status_code == 409
    assert second_response.json["success"] is False




def test_get_events():
    client = app.test_client()

    event = {
        "title": "DevOps Workshop",
        "date": "2027-03-15",
        "location": "Test Environment",
        "description": "Testing event listing",
    }

    create_response = client.post("/api/events", json=event)
    assert create_response.status_code == 201

    response = client.get("/api/events")

    assert response.status_code == 200
    event_titles = [item["title"] for item in response.json]
    assert "DevOps Workshop" in event_titles





 


def test_create_event():
    client = app.test_client()

    response = client.post(
        "/api/events",
        json={
            "title": "Pytest Automation Workshop Unique 2026",
            "date": "2027-01-15",
            "location": "Test Environment",
            "description": "Testing event creation with pytest"
        }
    )

    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["event"]["title"] == "Pytest Automation Workshop Unique 2026"


def test_create_event_missing_title():
    client = app.test_client()

    response = client.post(
        "/api/events",
        json={
            "date": "2026-12-05",
            "location": "Bengaluru",
            "description": "Learn Python basics"
        }
    )

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["message"] == "title is required."


def test_create_duplicate_event():
    client = app.test_client()

    event = {
        "title": "Duplicate Test Workshop",
        "date": "2027-02-20",
        "location": "Test Environment",
        "description": "Testing duplicate event prevention",
    }

    first_response = client.post("/api/events", json=event)
    second_response = client.post("/api/events", json=event)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json["success"] is False
    assert "already exists" in second_response.json["message"]


