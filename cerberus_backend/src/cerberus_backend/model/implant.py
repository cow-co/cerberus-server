import uuid

from sqlmodel import Field, SQLModel, create_engine

class Implant(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int
    is_active: bool