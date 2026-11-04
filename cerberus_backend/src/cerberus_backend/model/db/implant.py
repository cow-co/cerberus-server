import uuid

from sqlmodel import Field, Session, SQLModel, select

from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)


class Implant(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int
    is_active: bool


def get_all_db_implants() -> list[ImplantResponseDTO]:
    imps = []
    with Session(engine) as sesh:
        statement = select(Implant)
        results = sesh.exec(statement)
        for res in results:
            imps.append(ImplantResponseDTO(
                implant_id=res.id,
                hostname=res.hostname,
                ip_addr=res.ip_addr,
                major_ver=res.major_ver,
                minor_ver=res.minor_ver,
                is_active=res.is_active,
            ))
    return imps


def get_db_implant_by_id(imp_id: uuid.UUID) -> ImplantResponseDTO | None:
    imp = None
    with Session(engine) as sesh:
        statement = select(Implant).where(Implant.id == imp_id)
        results = sesh.exec(statement)
        res = results.first()
        imp = ImplantResponseDTO(
            implant_id=res.id,
            hostname=res.hostname,
            ip_addr=res.ip_addr,
            major_ver=res.major_ver,
            minor_ver=res.minor_ver,
            is_active=res.is_active,
        )
    return imp


def create_db_implant(beacon: Beacon) -> BeaconResponseDTO:
    res = None
    with Session(engine) as sesh:
        imp = Implant(
            id=beacon.implant_id,
            hostname=beacon.hostname,
            ip_addr=beacon.ip_addr,
            major_ver=beacon.major_ver,
            minor_ver=beacon.minor_ver,
            is_active=True,
        )
        sesh.add(imp)
        sesh.commit()
        sesh.refresh(imp)
        res = BeaconResponseDTO(
            implant_id=imp.id,
            tasks=[]    # TODO Get tasks for implant
        )
    return res
