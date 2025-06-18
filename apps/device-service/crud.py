from sqlalchemy.orm import Session

from models import Device, DeviceType
from schemas import DeviceTypeCreate, DeviceCreate


# Получение типа устройства
def get_device_type(db: Session, type_id: str):
    return db.query(DeviceType).filter(DeviceType.id == type_id).first()


# Создание типа устройства
def create_device_type(db: Session, device_type: DeviceTypeCreate):
    db_type = DeviceType(**device_type.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)

    device_type_id = db.query(DeviceType).filter(DeviceType.name == device_type.name).first()

    return str(device_type_id.id)


# Получение устройства
def get_device(db: Session, device_id: str):
    return db.query(Device).filter(Device.id == device_id).first()


# Создание устройства
def create_device(db: Session, device: DeviceCreate):
    db_device = Device(**device.dict(), is_online=False)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    res = db.query(Device).filter(Device.name == device.name).first()

    return {
        "id": str(res.id),
        "is_online": res.is_online,
        "last_seen": res.last_seen,
        "name": res.name,
        "serial_number": res.serial_number,
        "type_id": str(res.type_id),
        "house_id": str(res.house_id)
    }


# Удаление устройства
def delete_device(db: Session, device_id: str):
    db_device = get_device(db, device_id)

    if db_device:
        db.delete(db_device)
        db.commit()
        return True
    
    return False
