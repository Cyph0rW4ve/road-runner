from typing import Union, List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, CHAR, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel


DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost/road_runner"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class CargoTypes(Base):
    __tablename__ = "cargo_types"
    
    id = Column(CHAR(4), primary_key=True, index=True)
    cargo_name = Column(VARCHAR(255), nullable=False)
    cargo_type = Column(VARCHAR(255), nullable=False)

class Trucks(Base):
    __tablename__ = "trucks"
    
    id = Column(CHAR(4), primary_key=True, index=True)
    brand = Column(VARCHAR(255))  
    name = Column(VARCHAR(255))   
    fuel_tank = Column(Integer)    
    liters_per_100km = Column(Integer)  
    max_weight = Column(Integer)   


class CargoTypesResponse(BaseModel):
    id: str
    cargo_name: str
    cargo_type: str

    class Config:
        orm_mode = True

class TrucksResponse(BaseModel):
    id: str
    brand: str
    name: str
    fuel_tank: int
    liters_per_100km: int
    max_weight: int

    class Config:
        orm_mode = True

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/cargo_types/", response_model=List[CargoTypesResponse])
def read_cargo_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        cargo_types = db.query(CargoTypes).offset(skip).limit(limit).all()
        return cargo_types
    except Exception as e:
        print(f"Error fetching cargo types: {e}")  
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/trucks/", response_model=List[TrucksResponse])
def read_trucks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        truck_items = db.query(Trucks).offset(skip).limit(limit).all()
        return truck_items
    except Exception as e:
        print(f"Error fetching trucks: {e}")  
        raise HTTPException(status_code=500, detail="Internal Server Error")