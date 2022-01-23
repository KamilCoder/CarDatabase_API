from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Float, String


Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    make = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    avg_rating = Column(Float)
    rates_number = Column(Integer)
