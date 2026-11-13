from fastapi import APIRouter
from fastapi.logger import logger

router = APIRouter()


@router.get("")
def check_health() -> None:
    logger.info("Healthcheck called")
