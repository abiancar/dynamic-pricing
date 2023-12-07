from city import City
from trip import Trip

import random
import numpy
import datetime
import itertools
import math


philadelphia = City("Philadelphia", 1527886, temp=70, ue_rate=0.1, gas=3.5)
nyc = City("New York City", 7888121, temp=67, ue_rate=0.05, gas=5)
washington = City("Washington DC", 631693, temp=72, ue_rate=0.07, gas=4)
baltimore = City("Baltimore", 563455, temp=69, ue_rate=0.024, gas=3.37)
boston = City("Boston", 654776, temp=50, ue_rate=0.006, gas=5)


class Env:
    def __init__(self):
        self.cities = [philadelphia, nyc, washington, baltimore, boston]

        # Using list comprehension and Trip class to generate the upcoming trips
        self.upcoming_trips = []
        self.completed_trips = []
        possible_trip_combinations = [
            (origin, destination)
            for origin, destination in itertools.combinations(self.cities, 2)
        ]
        for i in range(50):
            comb = random.choice(possible_trip_combinations)
            orgdest = numpy.random.choice(
                comb, size=2, replace=False
            )  # from pair, randomly choose origin + destination
            self.upcoming_trips.append(Trip(orgdest[0], orgdest[1]))

        self.date = datetime.datetime.now()

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

        if (self.date.month // 3) + 1 in [1, 5]:
            av_temp = 30  # winter
        if (self.date.month // 3) + 1 == 2:
            av_temp = 55  # spring
        if (self.date.month // 3) + 1 == 3:
            av_temp = 80  # summer
        if (self.date.month // 3) + 1 == 4:
            av_temp = 55  # fall

        for city in self.cities:
            city.temp = (random.gauss(av_temp, 10) + city.temp) / 2

    ### for now we are keeping unemployment rate + pop fixed
