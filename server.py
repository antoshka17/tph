from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, FileResponse
from calculations import *
import time
from models import *
import random
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def main():
    return FileResponse('public/index.html')

@app.get('log')
def get_all_con(db: Session = Depends(get_db)):
    return db.query(Content).all()

@app.get('http://localhost:3306/db/log/{id}')
def get_con(id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id==id).first()
    if comp == None:
        return JSONResponse(status_code=404, content={"message": "nothing found"})
    return comp

@app.post('http://localhost:3306/db/log', response_model=Data)
def create_comp(data: Data, db: Session = Depends(get_db)):
    comp = Content(time=data.time, cpu_consumption=data.cpu_consumption,
                   ram_consumption=data.ram_consumption, total_consumption=data.total_consumption)
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp

@app.put('http://localhost:3306/db/log')
def update_comp(data: Data, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id == data.id).first()
    if comp == None:
        return JSONResponse(status_code=404, content={"message":"nothing found"})
    comp.time = data.time
    comp.cpu_consumption = data.cpu_consumption
    comp.ram_consumption = data.ram_consumption
    comp.total_consumption = data.total_consumption
    db.commit()
    db.refresh(comp)
    return comp

@app.delete('http://localhost:3306/db/log/{id}')
def delete_comp(id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id==id)
    if comp == None:
        return JSONResponse(status_code=404, content={'message':"nothing found"})
    db.delete(comp)
    db.commit()
    return comp

time_start = time.time()
curr_time = time.time()

while curr_time - time_start < 10:
    cpu_con, ram_con, total_con = calculate(cpu, ram)
    content_obj = Content(time=datetime.now(), cpu_consumption=cpu_con, ram_consumption=ram_con,
                          total_consumption=total_con)
    data = create_comp(content_obj, session())
    curr_time = time.time()
    print(data)
    req = get_con(random.randint(6, 250), session())
    print(req.id, req.time, req.cpu_consumption, req.ram_consumption, req.total_consumption)



