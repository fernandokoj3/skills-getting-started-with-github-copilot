import pytest

def test_signup_success(client, reset_activities):
    # Arrange: reset_activities fixture sets known state
    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]


def test_signup_activity_not_found(client):
    # Arrange/Act
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "test@mergington.edu"}
    )
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_registration(client, reset_activities):
    # Arrange
    email = "duplicate@mergington.edu"
    # Act
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


def test_signup_activity_at_capacity(client, reset_activities):
    # Arrange
    from src.app import activities
    activity = activities["Chess Club"]
    for i in range(activity["max_participants"] - len(activity["participants"])):
        activity["participants"].append(f"student{i}@mergington.edu")
    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "overcapacity@mergington.edu"}
    )
    # Assert
    assert response.status_code == 400
