from sqlmodel import create_engine, SQLModel, Session

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://todouser:todopass@localhost:5432/tododb"
)
engine = create_engine(DATABASE_URL, echo=True)

# Create database and dables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session