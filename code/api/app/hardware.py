from subprocess import Popen
import logging
log = logging.getLogger()


class TemperatureControl:

    def __init__(self, heater_pin: int):
        self.process = None
        self.heater_pin = heater_pin

    def start_experiment(self, temperature: int, snapshots_hr: int):
        log.info(f'Starting experiment with T: {temperature}C')
        self.temperature = temperature
        self.snapshots_hr = snapshots_hr
        self.start_temp_control()

    def start_temp_control(self):
        self.process = Popen(['/bin/bash', 'tcontrol.sh', str(self.heater_pin), str(self.temperature)])
    
    def stop_experiment(self):
        if self.process:
            log.info('Stopping experiment')
            self.process.send_signal(2)
            self.process.wait()
            self.process = None
