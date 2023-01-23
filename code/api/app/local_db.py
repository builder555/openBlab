from typing import List
from app.db_interfaces import ExperimentModel
from app.db_interfaces import ExperimentDBModel

class LocalDB:

    def __init__(self):
        self.experiments = []

    def add(self, experiment: ExperimentModel) -> int:
        experiment_id = len(self.experiments) + 1
        new_item = ExperimentDBModel(
            id=experiment_id,
            is_running=True,
            **experiment.dict()
        )
        self.experiments.append(new_item)
        return experiment_id

    def get(self, experiment_id: int) -> ExperimentDBModel:
        return self.experiments[experiment_id-1]

    def items(self) -> List[ExperimentDBModel]:
        return self.experiments
