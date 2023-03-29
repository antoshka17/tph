from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, Float
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
from eco2ai.tools.tools_cpu import CPU, all_available_cpu
from eco2ai.tools.tools_ram import RAM
import warnings
from eco2ai.utils import(
    is_file_opened,
    define_carbon_index,
    get_params,
    set_params,
    # calculate_money,
    # summary,
    encode,
    encode_dataframe,
    electricity_pricing_check,
    calculate_price,
    FileDoesNotExistsError,
    NotNeededExtensionError,
)

warnings.filterwarnings('ignore')
cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)

time_start = time.time()
curr_time = time.time()
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
Session = sessionmaker(engine)
while curr_time - time_start < 10:
    with Session() as session:
        cpu_con = cpu.get_consumption()
        ram_con = ram.get_consumption()
        total_con = ram_con + cpu_con
        curr_time = time.time()
        content = Content(time=datetime.now(), cpu_consumption=cpu_con, ram_consumption=ram_con,
                      total_consumption=total_con)
        session.add(content)
        session.commit()