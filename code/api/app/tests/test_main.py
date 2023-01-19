from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from app.main import _app, get_db, ExperimentModel, ExperimentDBModel, LocalDB

@pytest.fixture()
def client():
    LDB = LocalDB()
    def get_new_db():
        return LDB
    _app.dependency_overrides[get_db] = get_new_db
    client = TestClient(_app)
    return client

class TestMain:

    def test_ping(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}

    def test_start_new_experiment(self, client):
        experiment_data = {
            'specimen': 'R. stolonifer',
            'temperature': 37,
            'snapshots_hr': 2,
        }
        response = client.post("/experiments", json=experiment_data)
        assert response.status_code == 200
        assert response.json() == {"id": 1}

    def test_cannot_start_experiment_with_missing_data(self, client):
        experiment_data = {
            'specimen': 'R. stolonifer',
            'temperature': 37,
        }
        response = client.post("/experiments", json=experiment_data)
        assert response.status_code == 422
    
    def test_get_existing_experiment(self, client):
        experiment_data = {
            'specimen': 'R. stolonifer',
            'temperature': 40,
            'snapshots_hr': 3,
        }
        response = client.post("/experiments", json=experiment_data)
        response = client.get("/experiments/1")
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'is_running': True,
            **experiment_data
        }

    def test_cannot_start_experiment_when_one_is_running(self, client):
        experiment_data = {
            'specimen': 'R. stolonifer',
            'temperature': 37,
            'snapshots_hr': 2,
        }
        client.post("/experiments", json=experiment_data)
        response2 = client.post("/experiments", json=experiment_data)
        assert response2.status_code == 400

    def test_cannot_get_nonexistent_experiment(self, client):
        response = client.get("/experiments/1")
        assert response.status_code == 404
