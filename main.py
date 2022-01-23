from fastapi import FastAPI, Request
import requests,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Car, Base
from pydantic import BaseModel


engine = create_engine("sqlite:///./base.sqlite",echo=True)
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()

class RequestCar(BaseModel):
    make : str
    model : str

def createBase(engine):
    Base.metadata.create_all(engine)

def getMakesModelsData(make):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/'+make+'?format=json'
    data = requests.get(url).json()
    return data['Results']

@app.post('/cars') #ma być post!
def postCars(requestCar : RequestCar):
    modelsBase = [vehicle['Model_Name'] for vehicle in getMakesModelsData(requestCar.make)]
    if requestCar.model.capitalize() in modelsBase:
        car = Car(make=requestCar.make, model=requestCar.model)
        session.add(car)
        session.commit()
        return {'message':'Car saved to base'}
    else:
        return {'message':'Error - there is no car like '+car.make+' '+car.model}


@app.delete('/cars/{id}')
async def deleteCar(id):
    if Car.query.get(id):
        try:
            Car.delete(id) # DOKONCZYC
            db.session.commit()
            return {'msg':'Car deleted'}
        except:
            db.session.rollback()
    else:
        return {'error':"Car doesn't exist in db"}

@app.post('/rate')
async def rateCar():
    requestCarId = request.body['id']
    requestCarRating = request.body['rating'] #SPRAWDZIC
    car = Car.query.get(requestCarId)
    car.avg_rating+=requestCarRating
    car.ratingsCounter+=1
    try:
        db.session.add(car)
        db.session.commit()
    except:
        return {'error':'Error while rating car'}


@app.get('/cars')
def getCars():
    return session.query(Car).all()#zwraca liste - dopracowac


@app.get('/popular')
def getPopularCars():
    carList = session.query(Car).all()
    return session.query(Car).all()
