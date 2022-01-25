from fastapi import FastAPI, Request
import requests,json
from sqlalchemy import create_engine, desc
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

class RequestRate(BaseModel):
    car_id : int
    rating : int

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
        return {'message':'Error - there is no car like '+requestCar.make+' '+requestCar.model}


@app.delete('/cars/{id}')
async def deleteCar(id):
    if Car.query.get(id):
        try:
            session.delete(id) # DOKONCZYC
            session.commit()
            return {'msg':'Car deleted'}
        except:
            session.rollback()
    else:
        return {'error':"Car doesn't exist in db"}

@app.post('/rate')
async def rateCar(requestRate : RequestRate):
    car = Car.query.get(requestRate.car_id) #query get?
    car.rates_number+=1
    car.avg_rating = (car.avg_rating + requestRate.rating)/car.rates_number #dokonczyc obliczanie
    try:
        db.session.add(car)
        db.session.commit()
        return {'message':'OK'}
    except:
        session.rollback()
        return {'error':'Error while rating car'}


@app.get('/cars')
def getCars():
    carList = session.query(Car).all()
    return ({'id':car.id,'make':car.make,'model':car.model,'avg_rating':car.avg_rating} for car in carList)#zwraca liste - dopracowac


@app.get('/popular')
def getPopularCars():
    return session.query(Car).order_by('id'desc())

    #return ({'id':car.id,'make':car.make,'model':car.model,'avg_rating':car.avg_rating} for car in carList)
