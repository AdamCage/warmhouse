from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DeviceTypeCreate(BaseModel):
    name: str
    category: str
    protocol: str


class DeviceTypeResponse(DeviceTypeCreate):
    id: str


class DeviceCreate(BaseModel):
    name: str
    serial_number: str
    type_id: str
    house_id: str


class DeviceResponse(DeviceCreate):
    id: str
    is_online: bool
    last_seen: Optional[datetime]
