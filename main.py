from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    id: str
    brand: str
    model: str
    characteristics: Characteristic

cars: List[Car] = []

@app.get("/ping")
async def ping():
    return "pong"


@app.post("/cars", status_code=201)
async def create_car(car: Car):
    cars.append(car)
    return car


@app.get("/cars", response_model=List[Car])
async def get_cars():
    return cars


@app.get("/cars/{id}")
async def get_car(id: str):
    for car in cars:
        if car.id == id:
            return car
    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")

@app.put("/cars/{id}/characteristics")
async def update_car_characteristics(id: str, characteristics: Characteristic):
    for car in cars:
        if car.id == id:
            car.characteristics = characteristics
            return car
    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")