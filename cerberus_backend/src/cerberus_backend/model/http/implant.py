import uuid

from cerberus_backend.model.http.task import Task
from pydantic import BaseModel


class Beacon(BaseModel):
    implant_id: uuid.UUID | None = None
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int


class ImplantResponseDTO(BaseModel):
    implant_id: uuid.UUID | None
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int
    is_active: bool


class BeaconResponseDTO(BaseModel):
    implant_id: uuid.UUID | None
    tasks: list[Task] = []
