import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import _app
from app.main import get_db
from app.main import get_hardware
from app.local_db import LocalDB
from app.hardware import TemperatureControl

temp_control = TemperatureControl(heater_pin=17)


@pytest.fixture()
def client():
    test_db = LocalDB()
    _app.dependency_overrides[get_db] = lambda: test_db
    _app.dependency_overrides[get_hardware] = lambda: temp_control
    client = TestClient(_app)
    return client


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

@patch('app.hardware.Popen', new=MagicMock())
def test_start_new_experiment(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 200
    assert response.json() == {"id": 1}

@patch('app.hardware.Popen', new=MagicMock())
def test_stop_experiment(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    client.post("/experiments", json=experiment_data)
    response = client.put("/experiments/1/stop")
    assert response.status_code == 200
    assert response.json() == {"id": 1}

@patch('app.hardware.Popen', new=MagicMock())
def test_get_existing_experiment(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 40,
        'snapshots_hr': 3,
    }
    fake_datetime = 1675300000
    with patch('app.local_db.datetime') as mock_datetime:
        mock_datetime.now().timestamp.return_value = fake_datetime
        response = client.post("/experiments", json=experiment_data)
        response = client.get("/experiments/1")
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'is_running': True,
        **experiment_data,
        'started': fake_datetime,
        'snapshots':[],
        'temperatures':[],
    }

@patch('app.hardware.Popen', new=MagicMock())
def test_list_past_experiments(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 40,
        'snapshots_hr': 3,
    }
    fake_datetime = 1675300000
    with patch('app.local_db.datetime') as mock_datetime:
        mock_datetime.now().timestamp.return_value = fake_datetime
        client.post("/experiments", json=experiment_data)
    response = client.get("/experiments")
    assert response.status_code == 200
    assert response.json() == [{
        'id': 1,
        'is_running': True,
        'started': fake_datetime,
        **experiment_data
    }]

@patch('app.hardware.Popen', new=MagicMock())
def test_stopping_experiment_updates_database(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    fake_datetime = 1675300000
    with patch('app.local_db.datetime') as mock_datetime:
        mock_datetime.now().timestamp.return_value = fake_datetime
        client.post("/experiments", json=experiment_data)
    client.put("/experiments/1/stop")
    response = client.get("/experiments/1")
    assert response.status_code == 200
    assert response.json()['is_running'] == False

def test_cannot_stop_nonexistent_experiment(client):
    response = client.put("/experiments/53/stop")
    assert response.status_code == 404

def test_cannot_start_experiment_with_missing_data(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
    }
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 422

@patch('app.hardware.Popen', new=MagicMock())
def test_cannot_start_experiment_when_one_is_running(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    client.post("/experiments", json=experiment_data)
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 400

def test_cannot_get_nonexistent_experiment(client):
    response = client.get("/experiments/1")
    assert response.status_code == 404
