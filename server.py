from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from typing import Optional

from database import Base, Computer, Content, engine, session
from models import Data, DataForLeonid, DataForLeonidWithComputer, Unit

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# получение сессии
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


graph_router = APIRouter(tags=["graph"])


@graph_router.get("/co2", response_model=list[DataForLeonid])
def get_co2_for_graphic(unit: Unit, computer_id: Optional[int] = None, db: Session = Depends(get_db)):
    format = {
        "days": "%Y-%j",
        "weeks": "%Y-%U",
        "hours": "%Y-%j-%H",
        "years": "%Y",
        "minutes": "%Y-%j-%H-%i",
    }
    if computer_id is not None:
        query = select(
            func.DATE_FORMAT(Content.time, format[unit.name]).label("label"),
            func.avg(Content.co2).label("co2"),
            func.max(Content.co2).label("co2"),
            func.sum(Content.co2).label("co2"),
            func.min(Content.co2).label("co2"),
        ).group_by("label").filter(Content.comp_id==computer_id)
    else:
        query = select(
            func.DATE_FORMAT(Content.time, format[unit.name]).label("label"),
            func.avg(Content.co2).label("co2"),
            func.max(Content.co2).label("co2"),
            func.sum(Content.co2).label("co2"),
            func.min(Content.co2).label("co2"),
        ).group_by("label")
    column_avg = db.execute(query)
    arr_column = column_avg.all()
    data = [
        DataForLeonid(
            date=arr_column[i][0],
            value_avg=arr_column[i][1],
            value_max=arr_column[i][2],
            value_sum=arr_column[i][3],
            value_min=arr_column[i][4],
        )
        for i in range(len(arr_column))
    ]
    print(data)
    return data


# получение данных для построения графика
@graph_router.get("/consumption", response_model=list[DataForLeonid])
def get_vals_for_graphic(unit: Unit,computer_id: Optional[int] = None, db: Session = Depends(get_db)):
    format = {
        "days": "%Y-%j",
        "weeks": "%Y-%U",
        "hours": "%Y-%j-%H",
        "years": "%Y",
        "minutes": "%Y-%j-%H-%i",
    }
    if computer_id is not None:
        query = select(
            func.DATE_FORMAT(Content.time, format[unit.name]).label("label"),
            func.avg(Content.total_consumption).label("consumption"),
            func.max(Content.total_consumption).label("consumption"),
            func.sum(Content.total_consumption).label("consumption"),
            func.min(Content.total_consumption).label("consumption"),
        ).group_by("label").filter(Content.comp_id == computer_id)
    else:
        query = select(
            func.DATE_FORMAT(Content.time, format[unit.name]).label("label"),
            func.avg(Content.total_consumption).label("consumption"),
            func.max(Content.total_consumption).label("consumption"),
            func.sum(Content.total_consumption).label("consumption"),
            func.min(Content.total_consumption).label("consumption"),
        ).group_by("label")
    column_avg = db.execute(query)
    arr_column = column_avg.all()
    data = [
        DataForLeonid(
            date=arr_column[i][0],
            value_avg=arr_column[i][1],
            value_max=arr_column[i][2],
            value_sum=arr_column[i][3],
            value_min=arr_column[i][4],
        )
        for i in range(len(arr_column))
    ]
    print(data)
    return data


computer_router = APIRouter(tags=["computer"])


@computer_router.get("/", response_model=list[DataForLeonidWithComputer])
def get_all_comps(db: Session = Depends(get_db)):
    column = db.execute(
        select(
            Content.comp_id.label("label"),
            func.avg(Content.total_consumption).label("consumption"),
            func.max(Content.total_consumption).label("consumption"),
            func.sum(Content.total_consumption).label("consumption"),
            func.min(Content.total_consumption).label("consumption"),
            func.sum(Content.co2).label("consumption"),
            func.sum(Content.price).label("consumption"),
        ).group_by("label")
    ).all()
    print(column)
    data = [
        DataForLeonidWithComputer(
            id=column[i][0],
            name=f"{column[i][0]}",
            value_avg=column[i][1],
            value_max=column[i][2],
            value_sum=column[i][3],
            value_min=column[i][4],
            co2=column[i][5],
            price=column[i][6],
        )
        for i in range(len(column))
    ]
    return data


# добавление в таблицу компьютеров нового компьютера
@computer_router.post("/")
def create_comp(name: str, db: Session = Depends(get_db)):
    comp = Computer(name=name)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


consumption_router = APIRouter(tags=["consumption"])


# получение всех строчек главной таблицы
@consumption_router.get("/")
def get_all_consumptions(db: Session = Depends(get_db)):
    comps = db.query(Content).all()
    return comps


# получение всех строчек в главной таблице с определенным id компьютера
@consumption_router.get("/{comp_id}")
def get_comp(comp_id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.comp_id == comp_id).all()
    if comp == None:
        return JSONResponse(
            status_code=404, content={"message": "nothing found"}
        )
    print(comp)
    return comp


# создание новой записи в главной таблице (считывание энергопотребления)
@consumption_router.post("/{comp_id}")
def create_comp_con(comp_id, data: Data, db: Session = Depends(get_db)):
    comp = Content(
        comp_id=comp_id,
        time=data.time,
        cpu_consumption=data.cpu_consumption,
        ram_consumption=data.ram_consumption,
        total_consumption=data.total_consumption,
        co2=data.co2,
        price=data.price,
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


# обновление записи в главной таблице (не используется пока)
@consumption_router.put("/{comp_id}")
def update_comp(comp_id: int, data: Data, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id == comp_id).first()
    if comp == None:
        return JSONResponse(
            status_code=404, content={"message": "nothing found"}
        )
    comp.time = data.time
    comp.cpu_consumption = data.cpu_consumption
    comp.ram_consumption = data.ram_consumption
    comp.total_consumption = data.total_consumption
    comp.comp_id = data.comp_id
    db.commit()
    db.refresh(comp)
    return comp


# удаление записи из главной таблицы (пока не используется)
@consumption_router.delete("/comp/{comp_id}")
def delete_comp(comp_id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.comp_id == comp_id).all()
    if comp == None:
        return JSONResponse(
            status_code=404, content={"message": "nothing found"}
        )
    db.delete(comp)
    db.commit()
    return comp


app.include_router(graph_router, prefix="/graph")
app.include_router(computer_router, prefix="/computer")
app.include_router(consumption_router, prefix="/consumption")
