import random
import time
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse


LOCATION_TO_SENSOR = {
    "Living Room": "1",
    "Bedroom": "2",
    "Kitchen": "3"
}
SENSOR_TO_LOCATION = {v: k for k, v in LOCATION_TO_SENSOR.items()}


def _create_response(location: Optional[str] = None, sensor_id: Optional[str] = None) -> dict:
    if not location:
        location = SENSOR_TO_LOCATION.get(sensor_id, "Unknown")
    
    if not sensor_id:
        sensor_id = LOCATION_TO_SENSOR.get(location, "0")

    value = round(random.uniform(-30.0, 30.0), 1)
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    
    return {
        "value": value,
        "unit": "Celsius",
        "timestamp": timestamp,
        "location": location,
        "status": "active",
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "description": f"{location} temperature sensor"
    }


app = FastAPI()


@app.get("/temperature")
def get_temperature(location: str = Query(None), sensor_id: str = Query(None)):
    return JSONResponse(content=_create_response(location, sensor_id))


@app.get("/temperature/{sensor_id}")
async def get_temperature_by_id(sensor_id: str):
    return JSONResponse(content=_create_response(None, sensor_id))
