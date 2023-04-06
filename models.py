from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Unit(Enum):
    years: str = "years"
    days: str = 'days'
    weeks: str = 'weeks'
    hours: str = 'hours'
    minutes: str = 'minutes'


class DataForLeonid(BaseModel):
    class Config:
        orm_mode = True

    date: str
    value_avg: float
    value_min: float
    value_max: float
    value_sum: float

class Comp(BaseModel):
    class Config:
        orm_mode = True
    name: str

class Classroom(BaseModel):
    class Config:
        orm_mode = True
    name: str
    classroom: str

class DataForLeonidWithComputer(BaseModel):
    class Config:
        orm_mode = True

    name: str
    building: str
    classroom: str
    id: int
    value_avg: float
    value_min: float
    value_max: float
    value_sum: float
    co2: float
    price: float


class Data(BaseModel):
    class Config:
        orm_mode = True

    id: int
    comp_id: int
    time: datetime
    cpu_consumption: float
    ram_consumption: float
    total_consumption: float
    co2: float
    price: float


class DataDb(BaseModel):
    class Config:
        orm_mode = True

    time: datetime
    cpu_consumption: float
    ram_consumption: float
    total_consumption: float
