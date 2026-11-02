import uuid

from fastapi import APIRouter

from cerberus_backend.controller import implant_controller
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_implants() -> list[ImplantResponseDTO]:
    return implant_controller.get_all_implants()


@router.get("/{implant_id}")
def get_implant(implant_id: uuid.UUID) -> ImplantResponseDTO:
    imp = implant_controller.get_implant(implant_id)
    if not imp:
        raise NotFoundException(msg=f"Could not find implant with ID {implant_id}!")
    return imp


@router.post("/beacon")
def beacon(beacon: Beacon) -> BeaconResponseDTO:
    return implant_controller.handle_beacon(beacon)
