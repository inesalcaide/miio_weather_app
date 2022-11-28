from pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

# Connecting to database
CONNECTION_STRING = "mongodb://root:1234@mongodb_weather_db:27017/"
client = MongoClient(CONNECTION_STRING)
mydb = client["weather_db"]
collection = mydb["weather"]


# Get list of cities
@app.route("/cities")
def cities():
    cities_list = collection.distinct("city_name")

    if len(cities_list) == 0:
        return {"error": "No cities in the database"}

    return {"cities_names": cities_list}


# Get average temperature for next 5 days for a given city
@app.route("/temperature", methods=['GET'])
def temperature():
    # Validate city
    city = request.args.get("city")
    city = city.lower().capitalize()
    if not city:
        return {"error": "Missing city, parameter city required"}

    pipeline = [
        {"$match": {"city_name": city}},
        {"$project": {
            "_id": "$date",
            "avg_tmp": {"$round": [{"$avg": ["$max_temp", "$min_temp"]}, 1]},
            "tmp_unit": "$temp_unit"}
        },
        {"$sort": {"_id": 1}}
    ]

    return {"temperatures": list(collection.aggregate(pipeline))}


# Get list of 10 cities with the earliest sunrise for a given day
@app.route("/sunrise", methods=['GET'])
def sunrise():
    # Validate city
    day = request.args.get("day")
    if not day:
        return {"error": "Missing day, parameter day required"}

    pipeline = [
        {"$match": {"date": day}},
        {"$project": {
            "_id": "$city_name",
            "sunrise": "$sunrise"
        }},
        {"$sort": {"sunrise": 1}},
        {"$limit": 10}
    ]

    return {"cities": list(collection.aggregate(pipeline))}


# Get list of 10 cities with the less speed of wind (average of the next 5 days)
@app.route("/wind")
def wind():
    pipeline = [
        {"$match": {}},
        {"$group": {
            "_id": "$city_name",
            "w_unit": {"$first": "$wind_unit" },
            "avg_wind": {"$avg": "$wind"}
        }},
        {"$project": {
            "rounded_avg_wind": {"$round": ["$avg_wind", 1]},
            "wind_unit": "$w_unit"
        }},
        {"$sort": {"rounded_avg_wind": 1}},
        {"$limit": 10}
    ]

    return {"cities": list(collection.aggregate(pipeline))}


if __name__ == '__main__':
    app.run()


