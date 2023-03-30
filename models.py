from pydantic import BaseModel
from datetime import datetime

class Data(BaseModel):
    class Config:
        orm_mode = True
    id: int
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