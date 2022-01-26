# CarDatabase_API
Car Database using FastAPI with verification car make and model


## Table of contents
* [General info]
* [Technologies]
* [Setup]
* [Example of use]

## General info
This project is simple car database with make and model checking.
	
## Technologies
Project is created with Python
	
## Setup
To run this project, install it locally using npm:

```
$ git clone this repo
$ cd CarDatabase_API
$ uvicorn main:app
```

## Example of use
Application got few endpoints.

To get list of cars use:
```
GET request on http://localhost:8000/cars
```

To post car use:
```
POST request on http://localhost:8000/cars

Content-Type: application/json;charset=UTF-8

{

  "make" : "Volkswagen",

  "model" : "Golf",

} 
```

To delete car use:
```
DELETE request on http://localhost:8000/cars/{id}
```
To post rate of car use:
```
POST request on http://localhost:8000/rate

Content-Type: application/json;charset=UTF-8

{

  "car_id" : 1,

  "rating" : 5,

}
```

To get most popular cars (The biggest number of rates) use:
```
GET request on http://localhost:8000/popular
```
