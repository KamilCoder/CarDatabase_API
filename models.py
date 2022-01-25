from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Float, String


Base = declarative_base()

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    make = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    avg_rating = Column(Float, default=0)
    rates_number = Column(Integer, default=0)
    rate = relationship("Rate", backref="car")

class Rate(Base):
    __tablename__ = "rate"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    rate = Column(Integer, default=0)
    car_id = Column(Integer, ForeignKey('car.id'))
