import requests
from pymongo import MongoClient

# Connect to database
CONNECTION_STRING = "mongodb://root:1234@mongodb_weather_db:27017/"
client = MongoClient(CONNECTION_STRING)
mydb = client["weather_db"]
collection = mydb["weather"]

# Drop previous collections
collection.drop()

# list of districts in Portugal
CITIES_LIST = ["Aveiro", "Beja", "Braga", "Bragança", "Castelo Branco", "Coimbra", "Évora", "Faro", "Guarda", "Leiria",
               "Lisboa", "Portalegre", "Porto", "Santarém", "Setúbal", "Viana do Castelo", "Vila Real", "Viseu"]

cities_location_keys = []
api_key = "Q8MlGkXHpsvi486k1D7c9u7CqjGMiHDk"

# Lookup cities location keys in API
for city in CITIES_LIST:
    try:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}&language=pt"
        response = requests.get(url)
        response.raise_for_status()

        response = response.json()
        for i in response:
            if i["Country"]["ID"] == "PT":
                cities_location_keys.append({city: i["Key"]})
                break
    except Exception as error:
        print("ERROR")
        print(error)


def transform_timestamp_to_time(ts: str):
    x = (((ts.split("T"))[1].split("+"))[0]).split(":")
    time = f"{x[0]}:{x[1]}"
    return time


def transform_timestamp_to_date(ts: str):
    x = ts.split("T")
    return x[0]


def get_weather_info(info, city_name):
    return {
        "city_name": city_name,
        "date": transform_timestamp_to_date(info["Date"]),
        "sunrise": transform_timestamp_to_time(info["Sun"]["Rise"]),
        "max_temp": info["Temperature"]["Maximum"]["Value"],
        "min_temp": info["Temperature"]["Minimum"]["Value"],
        "temp_unit": info["Temperature"]["Minimum"]["Unit"],
        "wind": float(info["Day"]["Wind"]["Speed"]["Value"]),
        "wind_unit": info["Day"]["Wind"]["Speed"]["Unit"]
    }


# Lookup weather info for the next 5 days in API for cities location keys
for key in cities_location_keys:
    city_name = list(key.keys())[0]
    count = 1
    try:
        location_key = key[city_name]

        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={api_key}&details=true&metric=true"
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()

        for day in response["DailyForecasts"]:
            collection.insert_one(get_weather_info(day, city_name))
            city_name_index = collection.create_index("city_name")

    except Exception as error:
        print(error)
