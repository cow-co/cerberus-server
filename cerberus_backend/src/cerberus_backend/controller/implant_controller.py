

import uuid

from cerberus_backend.model.http.implant import Beacon, BeaconResponseDTO, ImplantResponseDTO


def handle_beacon(beacon: Beacon) -> BeaconResponseDTO:
    return BeaconResponseDTO(implant_id=uuid.uuid4())

def get_all_implants() -> list[ImplantResponseDTO]:
    return []

def get_implant(implant_id: uuid.UUID) -> ImplantResponseDTO | None:
    return None