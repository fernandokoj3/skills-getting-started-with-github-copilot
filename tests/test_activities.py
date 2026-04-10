import pytest

def test_get_activities(client):
    # Arrange: (fixtures handle setup)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_activities_have_required_fields(client):
    # Arrange
    response = client.get("/activities")
    activities = response.json()
    # Act & Assert
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)

def test_root_redirect(client):
    # Arrange/Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
