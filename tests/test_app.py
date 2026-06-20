from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # Ensure the email is not already in the activity
    activities[activity_name]["participants"] = [
        p for p in activities[activity_name]["participants"] if p != email
    ]

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert second_response.status_code == 400
    assert second_response.json() == {
        "detail": f"Student {email} is already signed up for {activity_name}"
    }

    assert activities[activity_name]["participants"].count(email) == 1
