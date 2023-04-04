from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Unit(Enum):
    years: str = "years"
    days: str = 'days'
    weeks: str = 'weeks'
    hours: str = 'hours'


class DataForLeonid(BaseModel):
    class Config:
        orm_mode = True

    date: str
    value_avg: float
    value_min: float
    value_max: float
    value_sum: float


class DataForLeonidWithComputer(BaseModel):
    class Config:
        orm_mode = True

    name: str
    value_avg: float
    value_min: float
    value_max: float
    value_sum: float


class Data(BaseModel):
    class Config:
        orm_mode = True

    id: int
    comp_id: int
    time: datetime
    cpu_consumption: float
    ram_consumption: float
    total_consumption: float


class DataDb(BaseModel):
    class Config:
        orm_mode = True

    time: datetime
    cpu_consumption: float
    ram_consumption: float
    total_consumption: float
