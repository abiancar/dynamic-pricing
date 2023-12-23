# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import pandas as pd
import os

# Set time period
start = datetime(2022, 1, 1)
end = datetime(2022, 12, 31)

# Create Point for each city
baltimore = ("baltimore", Point(39.2904, -76.6122, 10))
washington = ("washington_dc", Point(38.9072, -77.0369, 25))
new_york_city = ("new_york_city", Point(40.7128, -74.0060, 10))
philadelphia = ("philadelphia", Point(39.9526, -75.1652, 12))
boston = ("boston", Point(42.3601, -71.0589, 19))


cities = [baltimore, washington, new_york_city, philadelphia, boston]


if not os.path.isdir("./.weather_data"):
    os.mkdir("./.weather_data")


# Get daily data for 2022 in each city

for city in cities:
    data = Daily(city[1], start, end)
    data = data.fetch()
    data.to_csv(f"./.weather_data/{city[0]}_weather.csv")
