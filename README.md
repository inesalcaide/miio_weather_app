# Flask Weather App
A simple API to get weather information in all Portugal capital districts cities, built with Python, Flask, MongoDB and Docker.


This project contains different components:
- **app.py** : File used to create the Flask API and that containing all the endpoints.
- **load_database_data.py** : Script used to create and populate the MongoDB database (weather_db).
## How to run the project:
> docker compose build 

> docker compose up

## Endpoints documentation:

> GET /cities
 
- Gets a list of locations available for consulting
---
> GET /temperature

- Gets the average temperature for each day (in the next 5 days) for a given city chosen by the user

- #### URL Parameters: city
---
> GET /sunrise

- Gets a list of 10 cities with the earliest sunrise for a given day chosen by the user

- #### URL Parameters: day
---
> GET /wind

- Get list of 10 cities with the less speed of wind (average of the next 5 days) 