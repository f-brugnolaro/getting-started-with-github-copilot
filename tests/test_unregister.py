"""Tests for DELETE /activities/{activity_name}/unregister."""

from urllib.parse import quote


def test_unregister_from_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{activity_path}/unregister", params={"email": email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_from_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{activity_path}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_email_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    activity_path = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{activity_path}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
