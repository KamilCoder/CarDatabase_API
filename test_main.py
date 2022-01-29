from main import app
import requests, json
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_cars():
    response = client.get("/cars")
    assert response.status_code == 200

def test_post_car():
    response = client.post("/cars", json={
    'make':'Volkswagen',
    'model':'golf',
    })
    assert response.status_code == 200
    assert response.json() == {'message':'Car saved to base'}

def test_popular_cars():
    response = client.get('/popular')
    assert response.status_code == 200

def test_rate_car():
    idOfAddedCar = requests.get('http://localhost:8000/cars').json()
    id = str(idOfAddedCar[len(idOfAddedCar)-1]['id'])
    response = client.post('/rate', json={
    'car_id': id,
    'rating': 5
    })
    assert response.status_code == 200
    assert response.json() == {'message':'OK'}

def test_delete_car():
    idOfAddedCar = requests.get('http://localhost:8000/cars').json()
    id = str(idOfAddedCar[len(idOfAddedCar)-1]['id'])
    response = client.delete('/cars/'+id)
