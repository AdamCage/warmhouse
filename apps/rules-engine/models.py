import uuid

from sqlalchemy import Column, String, UUID, JSON, Boolean

from database import Base


class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String)
    enabled = Column(Boolean, default=True)
    house_id = Column(String)  # UUID в строке
    triggers = Column(JSON)    # Простой JSON для триггеров
    actions = Column(JSON)     # Простой JSON для действий
