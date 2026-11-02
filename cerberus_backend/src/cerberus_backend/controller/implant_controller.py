import uuid

from cerberus_backend.model.db.implant import (
    Implant,
    create_db_implant,
    get_all_db_implants,
    get_db_implant_by_id,
)
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException


def handle_beacon(beacon: Beacon) -> BeaconResponseDTO:
    if beacon.implant_id:
        imp = get_db_implant_by_id(beacon.implant_id)
        if not imp:
            raise NotFoundException(msg="Implant could not be found for beacon!")
        imp.hostname = beacon.hostname if beacon.hostname else imp.hostname
        imp.ip_addr = beacon.ip_addr if beacon.ip_addr else imp.ip_addr
        imp.major_ver = beacon.major_ver if beacon.major_ver else imp.major_ver
        imp.minor_ver = beacon.minor_ver if beacon.minor_ver else imp.minor_ver
        imp.is_active = True
        updated = create_db_implant(imp)
        return BeaconResponseDTO(implant_id=updated.id)
    else:
        imp = Implant(
            hostname=beacon.hostname,
            ip_addr=beacon.ip_addr,
            major_ver=beacon.major_ver,
            minor_ver=beacon.minor_ver,
            is_active=True,
        )
        created = create_db_implant(imp)
        return BeaconResponseDTO(implant_id=created.id)


def get_all_implants() -> list[ImplantResponseDTO]:
    response = []
    for imp in get_all_db_implants():
        response.append(
            ImplantResponseDTO(
                implant_id=imp.id,
                hostname=imp.hostname,
                ip_addr=imp.ip_addr,
                major_ver=imp.major_ver,
                minor_ver=imp.minor_ver,
                is_active=imp.is_active,
            )
        )
    return response


def get_implant(implant_id: uuid.UUID) -> ImplantResponseDTO | None:
    imp = get_db_implant_by_id(implant_id)
    if imp:
        return ImplantResponseDTO(
            implant_id=imp.id,
            hostname=imp.hostname,
            ip_addr=imp.ip_addr,
            major_ver=imp.major_ver,
            minor_ver=imp.minor_ver,
            is_active=imp.is_active,
        )
    return None
