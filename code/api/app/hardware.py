from abc import ABC
from abc import abstractmethod
import concurrent.futures
from time import sleep
from app.local_db import ExperimentDBModel

try: # prevent import error on non-rpi devices
    from RPi.GPIO import GPIO # type: ignore
except ImportError:
    GPIO = None

class SensorsInterface(ABC):
    @abstractmethod
    def get_temperature(self) -> float:
        pass

    @abstractmethod
    def heat_on(self):
        pass

    @abstractmethod
    def heat_off(self):
        pass

class Sensors(SensorsInterface):

    def __init__(self, pin: int, temp_sensor: str):
        self.temp_sensor = temp_sensor
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW) # type: ignore

    def get_temperature(self) -> float:
        with open(self.temp_sensor, 'r') as t:
            lines = t.readlines()
        temp = float(lines[1].split('t=')[1]) / 1000
        return temp

    def heat_on(self):
        GPIO.output(self.pin, GPIO.HIGH) # type: ignore

    def heat_off(self):
        GPIO.output(self.pin, GPIO.LOW) # type: ignore


class TemperatureControl:

    def __init__(self, sensors: SensorsInterface):
        self.sensors = sensors
        self.is_running = False
    
    def start_experiment(self, experiment: ExperimentDBModel):
        self.is_running = experiment.is_running
        self.temperature = experiment.temperature
        self.snapshots_hr = experiment.snapshots_hr
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.__run)

    def __run(self):
        while self.is_running:
            if self.sensors.get_temperature() < self.temperature:
                self.sensors.heat_on()
            else:
                self.sensors.heat_off()
            sleep(1)
