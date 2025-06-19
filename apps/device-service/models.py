import uuid

from sqlalchemy import Column, String, UUID, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    category = Column(String(50))  # (sensor, relay, controller)
    protocol = Column(String(20))  # (MQTT, Zigbee, CoAP)


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    serial_number = Column(String(50), unique=True)
    type_id = Column(UUID(as_uuid=True), ForeignKey("device_types.id"))
    house_id = Column(UUID(as_uuid=True))
    is_online = Column(BOOLEAN)
    last_seen = Column(TIMESTAMP)

    device_type = relationship("DeviceType")