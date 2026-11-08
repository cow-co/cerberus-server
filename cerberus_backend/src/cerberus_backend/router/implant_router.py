import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.logger import logger

from cerberus_backend.controller import implant_controller
from cerberus_backend.controller.dependencies import security_dependencies
from cerberus_backend.model.http.implant import (
    Beacon,
    BeaconResponseDTO,
    ImplantResponseDTO,
)
from cerberus_backend.model.http.user import UserResponseDTO
from cerberus_backend.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("")
def get_implants(
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> list[ImplantResponseDTO]:
    logger.info(f"{user.id} requesting to get all implants")
    return implant_controller.get_all_implants()


@router.get("/{implant_id}")
def get_implant(
    implant_id: uuid.UUID,
    user: Annotated[UserResponseDTO, Depends(security_dependencies.get_logged_in_user)],
) -> ImplantResponseDTO:
    logger.info(f"{user.id} requesting to get implant with ID {implant_id}")
    imp = implant_controller.get_implant(implant_id)
    if not imp:
        raise NotFoundException(msg=f"Could not find implant with ID {implant_id}!")
    return imp


# TODO Beacon endpoint does need at least _some_ auth around it.
@router.post("/beacon")
def beacon(beacon: Beacon) -> BeaconResponseDTO:
    return implant_controller.handle_beacon(beacon)
