from abc import ABC
from abc import abstractmethod
from typing import List
from pydantic import BaseModel

class ExperimentModel(BaseModel):
    specimen: str
    temperature: int
    snapshots_hr: int


class ExperimentDBModel(ExperimentModel):
    id: int
    is_running: bool

class Database(ABC):
    @abstractmethod
    def add(self, experiment: ExperimentModel) -> int:
        pass

    @abstractmethod
    def get(self, experiment_id: int) -> ExperimentDBModel:
        pass

    @abstractmethod
    def items(self) -> List[ExperimentDBModel]:
        pass
