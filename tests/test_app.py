from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index_html():
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list():
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)
    response_data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response_data
    assert "Programming Class" in response_data
    assert isinstance(response_data["Chess Club"], dict)
    assert response_data["Chess Club"]["description"]


def test_signup_for_activity_succeeds():
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "newstudent1@mergington.edu"
    url = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})
    response_data = response.json()

    # Assert
    assert response.status_code == 200
    assert response_data == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_for_activity_duplicate_email_returns_400():
    # Arrange
    activity_name = "Programming Class"
    encoded_activity_name = quote(activity_name, safe="")
    email = "duplicate_student@mergington.edu"
    url = f"/activities/{encoded_activity_name}/signup"

    client.post(url, params={"email": email})

    # Act
    duplicate_response = client.post(url, params={"email": email})
    duplicate_data = duplicate_response.json()

    # Assert
    assert duplicate_response.status_code == 400
    assert duplicate_data["detail"] == "Email already signed up for this activity"


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "student404@mergington.edu"
    url = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})
    response_data = response.json()

    # Assert
    assert response.status_code == 404
    assert response_data["detail"] == "Activity not found"
