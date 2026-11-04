import uuid

from sqlmodel import Field, Session, SQLModel, select

from cerberus_backend.model.db.db_setup import engine


class Implant(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hostname: str | None = None
    ip_addr: str | None = None
    major_ver: int
    minor_ver: int
    is_active: bool


def get_all_db_implants() -> list[Implant]: # TODO Return DTOs
    imps = []
    with Session(engine) as sesh:
        statement = select(Implant)
        results = sesh.exec(statement)
        for res in results:
            imps.append(res)
    return imps


def get_db_implant_by_id(imp_id: uuid.UUID) -> Implant | None: # TODO Return DTOs
    imp = None
    with Session(engine) as sesh:
        statement = select(Implant).where(Implant.id == imp_id)
        results = sesh.exec(statement)
        imp = results.first()
    return imp


def create_db_implant(imp: Implant) -> Implant: # TODO Take and Return DTOs
    with Session(engine) as sesh:
        sesh.add(imp)
        sesh.commit()
        sesh.refresh(imp)
    return imp
