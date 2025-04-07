from typing import Union, List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, CHAR, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import googlemaps
import drivertimecalculator



DATABASE_URL = "mysql+pymysql://root:MoneyInTheBank24!@localhost/road_runner"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

gmaps = googlemaps.Client(key="AIzaSyBT_yW-Nz6zIbKidF_WgaKG3o17xeOI6-c")


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

class DriversRoute(BaseModel):
    from_location: str
    to_location: str
    cargo_weight: float
    deadline: str
    truck: str


app = FastAPI()

def calculate_distance_and_duration(from_location: str, to_location: str):
    try: 
        directions_result = gmaps.directions(from_location, to_location)
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['value']

        return distance, duration
    except Exception as e:
        print(f"Error fetching directions: {e}")
        raise HTTPException(status_code=500, detail="Error calculating route")

@app.get("/")
def read_root():
    return {"Hello": "World"}

origins = [
    "http://localhost:3000",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculateRoute")
def return_calculated_route(driversRoute: DriversRoute):
    distance, duration = calculate_distance_and_duration(driversRoute.from_location, driversRoute.to_location)

    driver_time_calculator = drivertimecalculator.DriverTimeCalculator()
    total_duration = driver_time_calculator.calculate_time("D001", duration)
    return {
        "from": driversRoute.from_location,
        "to": driversRoute.to_location,
        "cargo_weight": driversRoute.cargo_weight,
        "deadline": driversRoute.deadline,
        "truck": driversRoute.truck,
        "distance": distance,
        "duration": total_duration
    }

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
