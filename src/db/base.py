"""Set up the sqlite db."""

from sqlalchemy import (
    Engine,
    text,
)
from sqlalchemy.orm import sessionmaker as SQLAlchemySession
from sqlmodel import (  # noqa
    Session,
    SQLModel,
    and_,
    create_engine,
    func,
    inspect,
    or_,
    select,
)

DBNAME = "wiki.db"


def execute_raw_statement(sql_statement: str, engine: Engine):
    result = []
    with SQLAlchemySession(engine)() as session:
        result = session.execute(text(sql_statement)).fetchall()
    return result


def execute_raw_statement_without_return(sql_statement: str, engine: Engine):
    with SQLAlchemySession(engine)() as session:
        session.execute(text(sql_statement))


def get_db_engine():
    sqlite_url = f"sqlite:///{DBNAME}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)
    return engine


def create_tables():
    engine = get_db_engine()
    SQLModel.metadata.create_all(engine)
