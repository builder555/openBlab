from abc import ABC
from abc import abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class ExperimentNotFoundException(Exception):
    pass

class ExperimentModel(BaseModel):
    specimen: str
    temperature: int
    snapshots_hr: int


class ExperimentDBModel(ExperimentModel):
    id: int
    is_running: bool
    started: Optional[int] = None


class ExperimentDetailsDBModel(ExperimentDBModel):
    snapshots: List[tuple]
    temperatures: List[tuple]


class DatabaseIface(ABC):
    @abstractmethod
    def add(self, experiment: ExperimentModel) -> int:
        pass

    @abstractmethod
    def get(self, experiment_id: int) -> ExperimentDBModel:
        pass

    @abstractmethod
    def items(self) -> List[ExperimentDBModel]:
        pass

    @abstractmethod
    def get_details(self, experiment_id: int) -> ExperimentDetailsDBModel:
        pass
