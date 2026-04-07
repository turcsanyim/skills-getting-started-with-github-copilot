def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_fails_for_unknown_activity(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_non_registered_participant(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-registered@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_keeps_other_participants_untouched(client):
    # Arrange
    activity_name = "Drama Club"
    removed_email = "isabella@mergington.edu"
    remaining_email = "james@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": removed_email},
    )
    activities = client.get("/activities").json()
    participants = activities[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert removed_email not in participants
    assert remaining_email in participants
