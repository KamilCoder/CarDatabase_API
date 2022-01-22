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

def getMakesModelData(make):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/'+make+'?format=json'
    data = requests.get(url).json()
    return data['results']

@app.post('/cars') #ma być post!
async def postCars():

    requestData = requests.body #dokonczyc
    return {'message':'car'+requestData['make']}
