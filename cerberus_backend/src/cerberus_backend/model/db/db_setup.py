from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

engine = create_engine("sqlite://", echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)


def setup_db():
    SQLModel.metadata.create_all(engine)
