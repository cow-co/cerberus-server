import uuid

from sqlmodel import Field, Session, SQLModel, select

from cerberus_backend.model.db.db_setup import engine
from cerberus_backend.model.db.task import Task
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)
from cerberus_backend.model.http.task import (
    TaskArgResponseDTO,
    TaskParamResponseDTO,
    TaskResponseDTO,
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
            imps.append(
                ImplantResponseDTO(
                    implant_id=res.id,
                    hostname=res.hostname,
                    ip_addr=res.ip_addr,
                    major_ver=res.major_ver,
                    minor_ver=res.minor_ver,
                    is_active=res.is_active,
                )
            )
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
        tasks = sesh.select(Task).where(Task.implant_id == imp.id)
        res = BeaconResponseDTO(
            implant_id=imp.id,
            tasks=[
                TaskResponseDTO(
                    id=t.id,
                    name=t.name,
                    implant_id=t.implant_id,
                    task_args=[
                        TaskArgResponseDTO(
                            id=a.id,
                            spec=TaskParamResponseDTO(
                                id=a.spec.id,
                                name=a.spec.name,
                                param_type=a.spec.param_type,
                            ),
                            value=a.value_str
                            if a.value_str
                            else (a.value_int if a.value_int else a.value_bool),
                        )
                        for a in t.task_args
                    ],
                )
                for t in tasks
            ],
        )
    return res
