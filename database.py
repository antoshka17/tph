from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import warnings

warnings.filterwarnings('ignore')

Base = declarative_base()

class Content(Base):
    __tablename__ = 'log'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    time = Column(DateTime(), nullable=False)
    cpu_consumption = Column(Float(), nullable=False)
    ram_consumption = Column(Float(), nullable=False)
    total_consumption = Column(Float(), nullable=False)

path = "mysql+pymysql://root:my-secret-pw@localhost:3307/db"
engine = create_engine(path, echo=True)
session = sessionmaker(engine)
