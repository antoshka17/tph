import warnings

from sqlalchemy import String, Integer, Column, DateTime, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

warnings.filterwarnings('ignore')

Base = declarative_base()


class Computer(Base):
    __tablename__ = 'computers'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(200))
    comp = relationship("Content", back_populates='comp')


# Child(parent_id=10)
# a = select(Parent).scalars().first()
# a.children
# Child(parent=a)
class Content(Base):
    __tablename__ = 'log'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    comp_id = Column(Integer(), ForeignKey('computers.id'))
    comp = relationship('Computer', back_populates='comp')
    time = Column(DateTime(), nullable=False)
    cpu_consumption = Column(Float(), nullable=False)
    ram_consumption = Column(Float(), nullable=False)
    total_consumption = Column(Float(), nullable=False)
    co2 = Column(Float(), nullable=False)
    price = Column(Float(), nullable=False)

    def __str__(self):
        return str(self.id) + " " + str(self.time) + " " + str(self.cpu_consumption) + " " + str(self.ram_consumption) \
               + " " + str(self.total_consumption)


path = "mysql+pymysql://root:my-secret-pw@localhost:3307/db"
engine = create_engine(path, pool_size=100, max_overflow=200)
session = sessionmaker(engine)
