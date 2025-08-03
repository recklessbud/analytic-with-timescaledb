import sqlmodel
from api.db.config import DATABASE_URL
from sqlmodel import SQLModel, Session


 
if DATABASE_URL == '':
    raise NotImplementedError('DATABASE_URL is not set')

engine = sqlmodel.create_engine(DATABASE_URL)

def initialize_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session