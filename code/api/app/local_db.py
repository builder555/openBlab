from typing import List
from app.db_interfaces import ExperimentModel
from app.db_interfaces import ExperimentDBModel
from app.db_interfaces import ExperimentDetailsDBModel
from datetime import datetime

class LocalDB:

    def __init__(self):
        self.experiments = []

    def add(self, experiment: ExperimentModel) -> int:
        experiment_id = len(self.experiments) + 1
        new_item = ExperimentDBModel(
            id=experiment_id,
            is_running=True,
            started=int(datetime.now().timestamp()),
            **experiment.dict()
        )
        self.experiments.append(new_item)
        return experiment_id

    def get(self, experiment_id: int) -> ExperimentDBModel:
        return self.experiments[experiment_id-1]
    
    def get_details(self, experiment_id: int) -> ExperimentDetailsDBModel:
        basic_info = self.get(experiment_id)
        snapshots = []
        temperatures = []
        return ExperimentDetailsDBModel(
            **basic_info.dict(),
            snapshots=snapshots,
            temperatures=temperatures,
        )

    def items(self) -> List[ExperimentDBModel]:
        return self.experiments
