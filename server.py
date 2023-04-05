from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from database import Base, engine, session, Content, Computer
from models import Data, DataForLeonid, Unit, DataForLeonidWithComputer

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


@app.get('/comps')
def get_all_comps(db: Session = Depends(get_db)):
    column = db.execute(
        select(
            Content.comp_id.label('label'),
            func.avg(Content.total_consumption).label("consumption"),
            func.max(Content.total_consumption).label("consumption"),
            func.sum(Content.total_consumption).label("consumption"),
            func.min(Content.total_consumption).label("consumption")).group_by("label")).all()
    print(column)
    data = [DataForLeonidWithComputer(name=f'{column[i][0]}', value_avg=column[i][1], value_max=column[i][2],
                                      value_sum=column[i][3], value_min=column[i][4]) for i in range(len(column))]
    return data


# получение данных для построения графика
@app.get('/vals')
def get_vals_for_graphic(unit: Unit, db: Session = Depends(get_db)):
    format = {
        'days': '%Y-%j',
        'weeks': '%Y-%U',
        'hours': '%Y-%j-%H',
        'years': '%Y'
    }
    column_avg = db.execute(select(func.DATE_FORMAT(Content.time, format[unit.name]).label("label"),
                                   func.avg(Content.total_consumption).label("consumption"),
                                   func.max(Content.total_consumption).label("consumption"),
                                   func.sum(Content.total_consumption).label("consumption"),
                                   func.min(Content.total_consumption).label("consumption")).group_by("label"))
    arr_column = column_avg.all()
    data = [DataForLeonid(date=arr_column[i][0], value_avg=arr_column[i][1], value_max=arr_column[i][2],
                          value_sum=arr_column[i][3], value_min=arr_column[i][4]) for i in range(len(arr_column))]
    print(data)
    return data


# получение всех строчек главной таблицы
@app.get('/comp')
def get_all_comps(db: Session = Depends(get_db)):
    comps = db.query(Content).all()
    return comps


# {
#   "label": "2020-03",
#   "cons": 30
# }

# получение всех строчек в главной таблице с определенным id компьютера
@app.get('/comp/{comp_id}')
def get_comp(comp_id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.comp_id == comp_id).all()
    if comp == None:
        return JSONResponse(status_code=404, content={"message": "nothing found"})
    print(comp)
    return comp


# создание новой записи в главной таблице (считывание энергопотребления)
@app.post('/comp/{comp_id}')
def create_comp_con(comp_id, data: Data, db: Session = Depends(get_db)):
    comp = Content(comp_id=comp_id, time=data.time, cpu_consumption=data.cpu_consumption,
                   ram_consumption=data.ram_consumption, total_consumption=data.total_consumption)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


# добавление в таблицу компьютеров нового компьютера
@app.post('/comp')
def create_comp(name: str, db: Session = Depends(get_db)):
    comp = Computer(name=name)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


# обновление записи в главной таблице (не используется пока)
@app.put('/comp')
def update_comp(data: Data, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id == data.id).first()
    if comp == None:
        return JSONResponse(status_code=404, content={"message": "nothing found"})
    comp.time = data.time
    comp.cpu_consumption = data.cpu_consumption
    comp.ram_consumption = data.ram_consumption
    comp.total_consumption = data.total_consumption
    comp.comp_id = data.comp_id
    db.commit()
    db.refresh(comp)
    return comp


# удаление записи из главной таблицы (пока не используется)
@app.delete('/comp/{comp_id}')
def delete_comp(comp_id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.comp_id == comp_id).all()
    if comp == None:
        return JSONResponse(status_code=404, content={'message': "nothing found"})
    db.delete(comp)
    db.commit()
    return comp
