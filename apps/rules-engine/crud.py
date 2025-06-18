from sqlalchemy.orm import Session

from schemas import ScenarioCreate
from models import Scenario


def create_scenario(db: Session, scenario: ScenarioCreate):
    db_scenario = Scenario(**scenario.dict())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    
    res = db.query(Scenario).filter(Scenario.name == scenario.name).first()

    return {"id": str(res.id)}


def get_scenarios(db: Session):
    return [
        {
            "id": str(s.id),
        }
        for s in db.query(Scenario).all()
    ]


def get_scenario(db: Session, scenario_id: str):
    return str(db.query(Scenario).filter(Scenario.id == scenario_id).first().id)


def update_scenario(db: Session, scenario_id: str, scenario_data: dict):
    db_scenario = get_scenario(db, scenario_id)
    if db_scenario:
        for key, value in scenario_data.items():
            setattr(db_scenario, key, value)
        db.commit()
        db.refresh(db_scenario)
        return db_scenario
    
    return None


def delete_scenario(db: Session, scenario_id: str):
    db_scenario = get_scenario(db, scenario_id)
    if db_scenario:
        db.delete(db_scenario)
        db.commit()
        return True
    
    return False
