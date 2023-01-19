from typing import List
from fastapi import FastAPI
from fastapi import Depends
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost',
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:8080',
]

_app = FastAPI()
_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class ExperimentModel(BaseModel):
    specimen: str
    temperature: int
    snapshots_hr: int

class ExperimentDBModel(ExperimentModel):
    id: int
    is_running: bool

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

db = LocalDB()

def get_db():
    return db

@_app.get('/ping')
def ping():
    return {"ping": "pong!"}

@_app.post('/experiments')
def start_new_experiment(experiment_data: ExperimentModel, db: LocalDB = Depends(get_db)):
    print('got db', db.items())
    is_running = any([v for v in db.items() if v.is_running])
    if is_running:
        raise HTTPException(status_code=400, detail="An experiment is already running")
    new_id = db.add(experiment_data)
    return {"id": new_id}

@_app.get('/experiments/{experiment_id}')
def get_existing_experiment(experiment_id: int, db = Depends(get_db)):
    try:
        return db.get(experiment_id)
    except:
        raise HTTPException(status_code=404, detail="Experiment not found")
