from subprocess import Popen
import logging
from app.local_db import ExperimentDBModel
log = logging.getLogger()


class TemperatureControl:

    def __init__(self, heater_pin: int):
        self.process = None
        self.heater_pin = heater_pin

    def start_experiment(self, experiment: ExperimentDBModel):
        log.info(f'Starting experiment with T: {experiment.temperature}C')
        self.temperature = experiment.temperature
        self.snapshots_hr = experiment.snapshots_hr
        self.start_temp_control()

    def start_temp_control(self):
        self.process = Popen(['/bin/bash', 'tcontrol.sh', str(self.heater_pin), str(self.temperature)])

    def __del__(self):
        try:
            SIGINT = 2
            if self.process:
                self.process.send_signal(SIGINT)
                self.process.wait()
        except:
            pass
