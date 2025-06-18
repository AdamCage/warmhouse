from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, engine
from schemas import ScenarioCreate, ScenarioResponse
from crud import create_scenario, get_scenarios, get_scenario, update_scenario, delete_scenario

from models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rules-Engine MVP")


@app.post("/scenarios", response_model=ScenarioResponse)
def create_new_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    return JSONResponse(content=create_scenario(db, scenario))


@app.get("/scenarios", response_model=list[ScenarioResponse])
def read_scenarios(db: Session = Depends(get_db)):
    return JSONResponse(content=get_scenarios(db))


@app.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
def read_scenario(scenario_id: str, db: Session = Depends(get_db)):
    scenario = get_scenario(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return JSONResponse(content={"id": scenario})
