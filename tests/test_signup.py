"""Tests for POST /activities/{activity_name}/signup."""

from urllib.parse import quote


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_for_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_for_activity_already_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{activity_path}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
