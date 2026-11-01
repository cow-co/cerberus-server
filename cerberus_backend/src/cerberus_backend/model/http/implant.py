

import uuid

from pydantic import BaseModel


class Beacon(BaseModel):
    implant_id: uuid.UUID | None = None
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int


class ImplantResponseDTO(BaseModel):
    implant_id: uuid.UUID
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int
    is_active: bool