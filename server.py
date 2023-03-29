from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import json
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

@app.get('http://localhost:3306/db/log')
def get_all_con(db: Session = Depends(get_db)):
    return db.query(Content).all()

@app.get('http://localhost:3306/db/log/{id}')
def get_con(id, db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id==id).first()
    print(type(comp))
    if comp == None:
        return JSONResponse(status_code=404, content={"message": "nothing found"})
    return comp

@app.post('http://localhost:3306/db/log')
def create_comp(data = Body(), db: Session = Depends(get_db)):
    data = json.loads(data)
    comp = Content(time=data["time"], cpu_consumption=data["cpu_consumption"],
                   ram_consumption=data["ram_consumption"], total_consumption=data["total_consumption"])
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp

@app.put('http://localhost:3306/db/log')
def update_comp(data=Body(), db: Session = Depends(get_db)):
    comp = db.query(Content).filter(Content.id == data['id']).first()
    if comp == None:
        return JSONResponse(status_code=404, content={"message":"nothing found"})
    comp.time = data['time']
    comp.cpu_consumption = data['cpu_consumption']
    comp.ram_consumption = data['ram_consumption']
    comp.total_consumption = data['total_consumption']
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

import time
from eco2ai.tools.tools_cpu import CPU
from eco2ai.tools.tools_ram import RAM
import warnings
warnings.filterwarnings('ignore')

cpu = CPU(cpu_processes='current', ignore_warnings=False)
ram = RAM(ignore_warnings=False)


time_start = time.time()
curr_time = time.time()
while curr_time - time_start < 10:
    cpu_con = cpu.get_consumption()
    ram_con = ram.get_consumption()
    total_con = ram_con + cpu_con
    curr_time = time.time()
    content_obj = Content(time=datetime.now(), cpu_consumption=cpu_con, ram_consumption=ram_con,
                           total_consumption=total_con)
    content_dict = {'id':content_obj.id, 'time':content_obj.time, 'cpu_consumption':content_obj.cpu_consumption,
                    'ram_consumption': content_obj.ram_consumption, 'total_consumption': content_obj.total_consumption}
    content_json = json.dumps(content_dict, default=str)
    print(content_json)
    data = create_comp(content_json, session())
    get_inf = get_con(100, session())
    print(data.id, data.time, data.cpu_consumption, data.ram_consumption, data.total_consumption)



