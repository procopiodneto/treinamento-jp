from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
import os

load_dotenv()

class Device(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    uptime: int = Field (default=0, index=True)
    contrato: str

class DeviceUpdate(SQLModel):
    nome: str | None = None
    uptime: int | None = None
    contrato: str | None = None

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

#decorador @app.on_event("startup") não é mais recomendado
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

#CREATE
@app.post("/devices/")
def create_device(device: Device, session: SessionDep) -> Device:
    session.add(device)
    session.commit()
    session.refresh(device)
    return device

#UPDATE
@app.patch("/devices/{device_id}", response_model=Device)
def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    session: SessionDep,
) -> Device:
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    
    entradas_atualizadas = device_update.model_dump(exclude_unset=True)
    for field, value in entradas_atualizadas.items():
        setattr(device, field, value)

    session.add(device)
    session.commit()
    session.refresh(device)

    return device

#READ
@app.get("/devices/")
def read_devices(
    session: SessionDep,
    offset: int=0,
    limit: Annotated[int, Query(le=50)] = 50,
) -> list[Device]:
    devices = session.exec(select(Device).offset(offset).limit(limit)).all()
    return devices

@app.get("/devices/{device_id}")
def read_device(device_id: int, session: SessionDep) -> Device:
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return device

#DELETE
@app.delete("/devices/{device_id}")
def delete_device(device_id: int, session: SessionDep):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    session.delete(device)
    session.commit()
    return {"ok": True}