from typing import List, Dict, Any

from pydantic import BaseModel


class ScenarioCreate(BaseModel):
    name: str
    description: str
    enabled: bool
    house_id: str
    triggers: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]


class ScenarioResponse(ScenarioCreate):
    id: str
