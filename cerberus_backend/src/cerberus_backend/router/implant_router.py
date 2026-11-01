from fastapi import APIRouter

from cerberus_backend.controller import implant_controller
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)

router = APIRouter()


@router.get()
def get_implants() -> list[ImplantResponseDTO]:
    return implant_controller.get_all_implants()


@router.post("/beacon")
def beacon(beacon: Beacon) -> BeaconResponseDTO:
    return implant_controller.handle_beacon(beacon)
