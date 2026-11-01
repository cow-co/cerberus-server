import cerberus_backend.controller.implant_controller as implant_controller
from cerberus_backend.model.db.db_setup import setup_db
from sqlmodel import SQLModel



def main() -> None:
    setup_db()
    implant_controller.get_all_implants()
    print("Hello from cerberus-backend!")
    