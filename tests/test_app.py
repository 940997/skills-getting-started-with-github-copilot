import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert expected_activity in data
    assert data[expected_activity]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    signup_url = "/activities/Chess%20Club/signup?email=newstudent%40mergington.edu"

    # Act
    response = client.post(signup_url)
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    signup_url = "/activities/Chess%20Club/signup?email=michael%40mergington.edu"

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_participant_removes_participant(client):
    # Arrange
    email = "daniel@mergington.edu"
    unregister_url = "/activities/Chess%20Club/participants?email=daniel%40mergington.edu"

    # Act
    response = client.delete(unregister_url)
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    unregister_url = "/activities/Chess%20Club/participants?email=unknown%40mergington.edu"

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_invalid_activity_returns_404_on_signup(client):
    # Arrange
    signup_url = "/activities/Unknown%20Club/signup?email=test%40mergington.edu"

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_invalid_activity_returns_404_on_unregister(client):
    # Arrange
    unregister_url = "/activities/Unknown%20Club/participants?email=test%40mergington.edu"

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
