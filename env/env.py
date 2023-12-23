from city.city import City
from trip.trip import Trip

import random
import numpy
import datetime
import itertools
import math


philadelphia = City("Philadelphia", 1527886, ue_rate=0.1, gas=3.5)
nyc = City("New York City", 7888121, ue_rate=0.05, gas=5)
washington = City("Washington DC", 631693, ue_rate=0.07, gas=4)
baltimore = City("Baltimore", 563455, ue_rate=0.024, gas=3.37)
boston = City("Boston", 654776, ue_rate=0.006, gas=5)


class Env:
    def __init__(self):
        self.cities = [philadelphia, nyc, washington, baltimore, boston]

        # Using list comprehension and Trip c  lass to generate the upcoming trips
        self.upcoming_trips = self.generate_trips(50)
        self.completed_trips = []
        self.date = datetime.datetime.now()

    def generate_trips(self, num_trips):
        possible_trip_combinations = list(itertools.combinations(self.cities, 2))
        return [
            Trip(*random.choice(possible_trip_combinations)) for _ in range(num_trips)
        ]

    def add_city(self, city):
        self.cities.append(city)

    def add_trip(self, origin_city, destination_city):
        self.upcoming_trips.append(Trip(origin_city, destination_city))

    def step(self):
        # update all the values in each city, simulating change that happens over time
        for city in self.cities:
            city.update_gas_prices()

        # for record-keeping, remove any trips that are completed
        for trip in self.upcoming_trips:
            assert len(self.upcoming_trips) > 0
            if self.date >= trip.departure_time:
                trip.calculate_demand()
                self.completed_trips.append(
                    self.upcoming_trips.pop(0)
                )  # we'd always be popping the first item in list if its datetime is greater than what we're looking for

        self.date += datetime.timedelta(days=1)
        self.update_temp()

    def score(self):
        total_demand = 0
        for trip in self.completed_trips:
            total_demand += trip.demand
        return math.sqrt(total_demand)

    def actions(self):
        lower = 0.99
        maintain = 1
        increase = 1.01
        # for trip in self.upcoming_trips:

        #     trip.average_cost = trip.average_cost * random.choice(
        #         [lower, maintain, increase]
        #     )

    def update_temp(self):
        # adding variability to daily temp

        temp_date = self.date.date()
        if temp_date.month == 2 and temp_date.day == 29:
            temp_date = datetime.date(2022, 2, 28)
        if temp_date.year != 2022:
            temp_date = datetime.date(2022, temp_date.month, temp_date.day)

        for city in self.cities:
            city.temp = random.gauss(city.get_temp(temp_date), 1)

    ### for now we are keeping unemployment rate + pop fixed

    def get_city(self, name):
        for city in self.cities:
            if city.name == name:
                return city
