from abc import ABC
from abc import abstractmethod
import concurrent.futures
from time import sleep
import glob
import logging as log
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


class TemperatureSensor(ABC):
    @abstractmethod
    def get_temperature(self) -> float:
        pass


class DS18B20(TemperatureSensor):
    def __init__(self, resolution: int = 12):
        devices = glob.glob('/sys/bus/w1/devices/28*')
        if len(devices) == 0:
            raise Exception('No temperature sensor found')
        self.temp_sensor = devices[0] + '/w1_slave'
        self.set_resolution(resolution)

    def get_temperature(self) -> float:
        with open(self.temp_sensor, 'r') as t:
            lines = t.readlines()
        temp = float(lines[-1].split('t=')[1]) / 1000
        return temp

    def set_resolution(self, resolution: int):
        if resolution not in [9, 10, 11, 12]:
            raise Exception('Invalid resolution')
        with open(self.temp_sensor, 'w') as t:
            t.write(f'{resolution}')


class Sensors(SensorsInterface):

    def __init__(self, heater_pin: int, temp_sensor: TemperatureSensor):
        self.temp_sensor = temp_sensor
        self.pin = heater_pin
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW) # type: ignore

    def get_temperature(self) -> float:
        return self.temp_sensor.get_temperature()

    def heat_on(self):
        GPIO.output(self.pin, GPIO.HIGH) # type: ignore

    def heat_off(self):
        GPIO.output(self.pin, GPIO.LOW) # type: ignore


class TemperatureControl:

    def __init__(self, sensors: SensorsInterface):
        self.sensors = sensors
        self.is_running = False

    def start_experiment(self, experiment: ExperimentDBModel):
        log.info(f'Starting experiment with T: {experiment.temperature}C')
        self.is_running = experiment.is_running
        self.temperature = experiment.temperature
        self.snapshots_hr = experiment.snapshots_hr
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.__run)

    def __run(self):
        while self.is_running:
            cur_temp = self.sensors.get_temperature()
            log.info(f'Current temperature: {cur_temp}C')
            if cur_temp < self.temperature:
                log.info('heat on')
                self.sensors.heat_on()
            else:
                log.info('heat off')
                self.sensors.heat_off()
            sleep(1)
