from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
from schemas import DeviceCreate, DeviceResponse, DeviceTypeCreate, DeviceTypeResponse
from crud import create_device, get_device, delete_device, create_device_type


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Device-Service MVP")


@app.post("/device-types", response_model=DeviceTypeResponse)
def create_type(type_data: DeviceTypeCreate, db: Session = Depends(get_db)):
    response = {"id": create_device_type(db, type_data)}
    return JSONResponse(content=response)


@app.post("/devices", response_model=DeviceResponse)
def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, device)


@app.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device_info(device_id: str, db: Session = Depends(get_db)):
    device = get_device(db, device_id)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return DeviceResponse(
        id=str(device.id),
        is_online=device.is_online,
        last_seen=device.last_seen,
        name=device.name,
        serial_number=device.serial_number,
        type_id=str(device.type_id),
        house_id=str(device.house_id)
    )


@app.delete("/devices/{device_id}")
def remove_device(device_id: str, db: Session = Depends(get_db)):
    success = delete_device(db, device_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return JSONResponse(content={"message": "Device deleted"})
