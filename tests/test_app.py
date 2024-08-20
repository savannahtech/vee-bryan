from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_interaction_happy_path(setup_database, db_session):
    response = client.post(
        "/api/interactions",
        json={"input_text": "Example input", "output_text": "Example output"},
    )

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert json_response["data"]["input"] == "Example input"
    assert json_response["data"]["output"] == "Example output"
    assert json_response["message"] == "Interaction created successfully"


def test_create_interaction_sad_path(setup_database, db_session):
    response = client.post(
        "/api/interactions", json={"input_text": None, "output_text": "Example output"}
    )

    assert response.status_code == 422  # Unprocessable Entity


def test_get_interactions_happy_path(setup_database, db_session):
    response = client.get("/api/interactions")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert isinstance(json_response["data"], list)
    assert json_response["message"] == "Interactions fetched successfully"


def test_get_alerts_happy_path(setup_database, db_session):
    response = client.get("/api/alerts")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert isinstance(json_response["data"], list)
    assert json_response["message"] == "Alerts fetched successfully"


def test_get_alerts_with_interaction_id_happy_path(setup_database, db_session):
    # Create an interaction first
    client.post(
        "/api/interactions",
        json={"input_text": "Example input", "output_text": "Example output"},
    )

    # Fetch alerts with interaction_id
    response = client.get("/api/alerts?interaction_id=1")

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert isinstance(json_response["data"], list)
    assert json_response["message"] == "Alerts fetched successfully"


def test_upload_csv_happy_path(setup_database, db_session):
    csv_content = (
        "Input,Output\n"
        "What is Deepchecks?,Deepchecks is an LLM Evaluation Tool\n"
        "When was Deepchecks founded?,Deepchecks was founded in 2024\n"
    )

    response = client.post(
        "/api/interactions/bulk", files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert (
        json_response["message"] == "CSV file received. Processing in the background."
    )


def test_upload_csv_sad_path(setup_database, db_session):
    csv_content = "Invalid CSV content"

    response = client.post(
        "/api/interactions/bulk", files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    json_response = response.json()

    assert json_response["success"] is True
    assert (
        json_response["message"] == "CSV file received. Processing in the background."
    )
    # The success here is about receiving the file; actual processing will fail, which is handled in the background.
