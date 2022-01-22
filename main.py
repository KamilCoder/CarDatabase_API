from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests,json,request

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app = FastAPI()

class Car(db.Model):
    id = db.Integer
    make = db.String
    model = db.String
    avg_rating = db.Float

def getMakesModelData(make):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/'+make+'?format=json'
    data = requests.get(url).json()
    return data['results']

@app.post('/cars') #ma być post!
async def postCars():

    requestData = requests.body #dokonczyc
    return {'message':'car'+requestData['make']}

@app.delete('/cars/'{id})
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
async def getCars():
    pass


@app.get('/popular')
async def getPopularCars():
    pass
