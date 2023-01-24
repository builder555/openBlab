import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import _app
from app.main import get_db
from app.main import get_hardware
from app.local_db import LocalDB
from app.hardware import TemperatureControl
from app.hardware import SensorsInterface

mock_sensors = MagicMock(spec=SensorsInterface)
temp_control = TemperatureControl(mock_sensors)
BadSensors = MagicMock(spec=SensorsInterface, side_effect=Exception)

@pytest.fixture()
def client():
    mock_sensors.reset_mock()
    test_db = LocalDB()
    _app.dependency_overrides[get_db] = lambda: test_db
    _app.dependency_overrides[get_hardware] = lambda: temp_control
    client = TestClient(_app)
    return client


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_start_new_experiment(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 200
    assert response.json() == {"id": 1}

def test_cannot_start_experiment_with_missing_data(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
    }
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 422

def test_get_existing_experiment(client):
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

@patch('concurrent.futures.ThreadPoolExecutor')
@patch('app.hardware.sleep')
def test_new_experiment_turns_on_heater_if_temperature_is_low(mock_sleep, mock_executor, client):
    def stop_experiment(*a,**kw):
        temp_control.is_running = False
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    mock_sensors.get_temperature.return_value = 35
    mock_sleep.side_effect = stop_experiment
    mock_executor.return_value.__enter__.return_value.submit = lambda run: run()
    client.post("/experiments", json=experiment_data)
    assert mock_sensors.heat_on.called

@patch('concurrent.futures.ThreadPoolExecutor')
@patch('app.hardware.sleep')
def test_new_experiment_turns_off_heater_if_temperature_is_high(mock_sleep, mock_executor, client):
    def stop_experiment(*a,**kw):
        temp_control.is_running = False
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 30,
        'snapshots_hr': 2,
    }
    mock_sensors.get_temperature.return_value = 35
    mock_sleep.side_effect = stop_experiment
    mock_executor.return_value.__enter__.return_value.submit = lambda run: run()
    client.post("/experiments", json=experiment_data)
    assert mock_sensors.heat_off.called
    assert not mock_sensors.heat_on.called

@patch('app.main.Sensors', new=BadSensors)
def test_starting_new_experiment_without_hardware_returns_error(client):
    experiment_data = {
        'specimen': 'R. stolonifer',
        'temperature': 37,
        'snapshots_hr': 2,
    }
    _app.dependency_overrides[get_hardware] = get_hardware
    response = client.post("/experiments", json=experiment_data)
    assert response.status_code == 500
    assert response.json() == {'detail': 'Hardware not available'}
