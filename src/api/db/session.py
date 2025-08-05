import sqlmodel
from api.db.config import DATABASE_URL
from sqlmodel import SQLModel, Session, text
import timescaledb
  
if DATABASE_URL == '':
    raise NotImplementedError('DATABASE_URL is not set')

engine = timescaledb.create_engine(DATABASE_URL, timezone='UTC', pool_pre_ping=True, pool_recycle=300)

def initialize_db():
    
    SQLModel.metadata.create_all(engine)
    try:
        timescaledb.metadata.create_all(engine)
        print("TimescaleDB tables created successfully")
    except Exception as e:  
        print(f"TimescaleDB setup error: {e}") 
        # Continue without TimescaleDB features if needed
  

def get_session():
    with Session(engine) as session:
        yield session
 