import uuid

from cerberus_backend.model.db.implant import (
    create_db_implant,
    get_all_db_implants,
    get_db_implant_by_id,
)
from cerberus_backend.model.db.task import get_db_tasks_for_implant
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)
from cerberus_backend.model.http.task import TaskResponseDTO
from cerberus_backend.utils.exceptions import NotFoundException


def handle_beacon(beacon: Beacon) -> BeaconResponseDTO:
    return create_db_implant(beacon)


def get_all_implants() -> list[ImplantResponseDTO]:
    return get_all_db_implants()


def get_implant(implant_id: uuid.UUID) -> ImplantResponseDTO | None:
    return get_db_implant_by_id(implant_id)


def get_implant_tasks(implant_id: uuid.UUID) -> list[TaskResponseDTO]:
    imp = get_implant(implant_id)
    if not imp:
        raise NotFoundException("Implant does not exist!")
    return get_db_tasks_for_implant(implant_id)