import pytest
import glob
from unittest.mock import MagicMock, mock_open, patch
from app.hardware import Sensors, DS18B20

GPIO = MagicMock()

@pytest.fixture
def ds18b20():
    with patch('glob.glob', return_value=['/sys/bus/w1/devices/28*']), \
        patch('builtins.open', mock_open(read_data='t=25000\n')), \
        patch('app.hardware.GPIO', new=GPIO):
        yield DS18B20()

@pytest.fixture
def sensors(ds18b20):
    return Sensors(heater_pin=5, temp_sensor=ds18b20)

def test_ds18b20_abstract_methods(ds18b20: DS18B20):
    assert callable(ds18b20.get_temperature) == True
    assert callable(ds18b20.set_resolution) == True

def test_ds18b20_init(ds18b20: DS18B20):
    with patch('glob.glob', return_value=['/sys/bus/w1/devices/28*']):
        assert ds18b20.temp_sensor == '/sys/bus/w1/devices/28*/w1_slave'

def test_ds18b20_get_temperature(ds18b20: DS18B20):
    with patch('builtins.open', mock_open(read_data='t=25000\n')) as mock_file:
        assert ds18b20.get_temperature() == 25.0
        mock_file.assert_called_once_with(ds18b20.temp_sensor, 'r')

def test_ds18b20_set_resolution(ds18b20: DS18B20):
    with patch('builtins.open', mock_open()) as mock_file:
        ds18b20.set_resolution(12)
        mock_file.assert_called_once_with(ds18b20.temp_sensor, 'w')
        mock_file().write.assert_called_once_with('12')

def test_ds18b20_set_resolution_invalid(ds18b20: DS18B20):
    with pytest.raises(Exception) as excinfo:
        ds18b20.set_resolution(13)
    assert str(excinfo.value) == 'Invalid resolution'

def test_sensors_get_temperature(sensors: Sensors):
    ds18b20 = sensors.temp_sensor
    with patch.object(ds18b20, 'get_temperature', return_value=25.0) as mock_temp:
        assert sensors.get_temperature() == 25.0
        mock_temp.assert_called_once()

def test_sensors_heat_on_off(sensors: Sensors):
    with patch('builtins.open', mock_open(read_data='t=25000\n')):
        sensors.heat_on()
        GPIO.output.assert_called_once_with(sensors.pin, GPIO.HIGH)
        sensors.heat_off()
        GPIO.output.assert_called_with(sensors.pin, GPIO.LOW)
