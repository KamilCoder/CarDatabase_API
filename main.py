from fastapi import FastAPI, Request, Response
import requests,json
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Car, Base, Rate
from pydantic import BaseModel


engine = create_engine("sqlite:///./base.sqlite?check_same_thread=False",echo=True)
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

@app.get('/')
def index():
    return '''<html><h1>'Welcome in Car Database API app'</h1></html>'''

@app.post('/cars')
def postCars(requestCar : RequestCar):
    modelsBase = [vehicle['Model_Name'] for vehicle in getMakesModelsData(requestCar.make)]
    if requestCar.model.capitalize() in modelsBase:
        try:
            car = Car(make=requestCar.make.capitalize(), model=requestCar.model.capitalize())
            session.add(car)
            session.commit()
            return {'message':'Car saved to base'}
        except:
            session.rollback()
            return {'message':'Error while saving car to base'}
    else:
        return {'message':'Error - there is no car like '+requestCar.make+' '+requestCar.model}


@app.delete('/cars/{id}')
def deleteCar(id):
    car = session.query(Car).get(id)
    if car:
        try:
            session.delete(car) # DOKONCZYC
            session.commit()
            return {'msg':'Car deleted'}
        except:
            session.rollback()
    else:
        return {'error':"Car doesn't exist in db"}

@app.post('/rate')
def rateCar(requestRate : RequestRate):
    car = session.query(Car).get(requestRate.car_id)
    if car:
        car.rate.append(Rate(rate=requestRate.rating))
        car.rates_number+=1
        car.avg_rating = float(sum([rating.rate for rating in car.rate])/car.rates_number)
        try:
            session.add(car)
            session.commit()
            return {'message':'OK'}
        except:
            session.rollback()
            return {'error':'Error while rating car'}
    else:
        return {'error':"car doesn't exist in database"}


@app.get('/cars')
def getCars():
    carList = session.query(Car).all()
    return({'id':car.id,'make':car.make,'model':car.model,'avg_rating':car.avg_rating} for car in carList)


@app.get('/popular')
def getPopularCars():
    carList = session.query(Car).order_by(Car.rates_number.desc())
    session.rollback()
    return ({'id':car.id,'make':car.make,'model':car.model,'rates_number':car.rates_number} for car in carList)
