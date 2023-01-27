from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.local_db import ExperimentModel
from app.local_db import LocalDB
from app.hardware import TemperatureControl
import logging
import os

log_level = os.environ.get('LOG_LEVEL', 'WARNING').upper()
log_level = log_level if log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] else 'WARNING'
logging.basicConfig(level=getattr(logging, log_level))
logging.getLogger().setLevel(getattr(logging, log_level))
log = logging.getLogger()
log.info(f'set logging level to {log_level}')

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

db = LocalDB()

def get_db():
    return db

def get_hardware():
    return TemperatureControl(heater_pin=17)

@_app.get('/ping')
def ping():
    return {"ping": "pong!"}

@_app.post('/experiments')
async def start_new_experiment(experiment_data: ExperimentModel, 
                         db: LocalDB = Depends(get_db), 
                         hw: TemperatureControl = Depends(get_hardware)):
    is_running = any([v for v in db.items() if v.is_running])
    if is_running:
        raise HTTPException(status_code=400, detail="An experiment is already running")
    new_id = db.add(experiment_data)
    hw.start_experiment(db.get(new_id))
    return {"id": new_id}

@_app.get('/experiments/{experiment_id}')
def get_existing_experiment(experiment_id: int, db = Depends(get_db)):
    try:
        return db.get(experiment_id)
    except:
        raise HTTPException(status_code=404, detail="Experiment not found")
