from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from cerberus_backend.model.common.settings import config

engine = create_engine(
    config.DB_CONNECT_STRING,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def setup_db():
    SQLModel.metadata.create_all(engine)
