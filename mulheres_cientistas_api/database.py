from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

from mulheres_cientistas_api.config import settings


def _fk_constraint_on(dbapi_con, con_record):
    dbapi_con.execute("PRAGMA foreign_keys = ON")


engine = create_engine(f"sqlite:///{settings.DATABASE_NAME}.db", echo=True)
event.listen(engine, "connect", _fk_constraint_on)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
