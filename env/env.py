import random
import datetime
import itertools
import math

import gymnasium as gym
import numpy as np
from city.city import City
from trip.trip import Trip


# Custom environment for RL agent, compatible with Gymnasium
class CustomEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.num_trips = 10
        # Initialize cities
        self.cities = []
        self.upcoming_trips = []
        self.completed_trips = []
        self.date = datetime.datetime(2023, 12, 25, 11, 57, 13, 751854)
        self.start_date = self.date

        # Define action and observation spaces
        self.action_space = gym.spaces.Box(
            low=0.0000, high=300.000, shape=(self.num_trips,), dtype=np.float32
        )
        single_trip_lower_bounds = np.array([0, 0, 0, 0, -30, -30])
        single_trip_upper_bounds = np.array([4, 4, float("inf"), 7, 100, 100])
        lower_bounds = np.tile(single_trip_lower_bounds, (self.num_trips, 1))
        upper_bounds = np.tile(single_trip_upper_bounds, (self.num_trips, 1))
        self.observation_space = gym.spaces.Box(
            low=lower_bounds, high=upper_bounds, dtype=np.float32
        )

    def step(self, action):
        # city data is up to date. We need to get the data for tomorrow
        assert len(self.upcoming_trips) == 10
        # print(action)
        assert self.action_space.contains(action), "Action out of bounds"

        self.update_prices(action)
        reward = self.score()  # Calculate reward (profit)

        obs = self._next_observation()  # Get the next observation, add more trips
        assert self.observation_space.contains(obs), "Observation out of bounds"

        # Check if a year has passed to determine if the episode is done
        done = self.date >= self.start_date + datetime.timedelta(days=365)
        truncate = False
        info = {
            "done": done,
            "truncate": truncate,
            # "obss": obs,
            "reward": reward,
            "actions": action,
        }
        return obs, reward, done, truncate, info

    # Reset the environment to its initial state
    def reset(self, **kwargs):
        self.cities = [
            City("Philadelphia", 1527886, ue_rate=0.1, gas=3.4, id=0),
            City("New York City", 7888121, ue_rate=0.05, gas=3.3, id=1),
            City("Washington DC", 631693, ue_rate=0.07, gas=3.274, id=2),
            City("Baltimore", 563455, ue_rate=0.024, gas=3.2, id=3),
            City("Boston", 654776, ue_rate=0.006, gas=3.274, id=4),
        ]
        self.start_date = datetime.datetime(2023, 12, 25, 11, 57, 13, 751854)
        self.date = self.start_date
        self.upcoming_trips.clear()
        self.completed_trips.clear()
        return (
            self._next_observation(),
            {},
        )  # Return the initial state of the environment

    # Format the observation data for the RL agent
    def _next_observation(self):
        # Create an observation array with features of each trip
        self.update_city_info()  # Update environmental factors
        self.date += datetime.timedelta(days=1)  # Advance the simulation by one day
        self.generate_trips(10)  # Generate new trips for the day
        observation = [self.format_trip_data(trip) for trip in self.upcoming_trips]
        return np.array(observation)

    # Helper method to format data for a single trip
    def format_trip_data(self, trip):
        # Format and return the data for a given trip
        trip_data = [
            np.float32(trip.origin.id),
            np.float32(trip.destination.id),
            np.float32(self.date.timestamp()),
            np.float32(trip.origin.gas_prices),
            np.float32(trip.origin.temp),
            np.float32(trip.destination.temp),
        ]
        return trip_data

    # Generate a specified number of trips between cities
    def generate_trips(self, num_trips):
        # Create trip combinations between cities
        combinations = list(itertools.combinations(self.cities, 2))
        for _ in range(num_trips):
            origin, destination = random.choice(combinations)
            self.add_trip(origin, destination)

    # Add a new trip to the upcoming trips list
    def add_trip(self, origin_city, destination_city):
        self.upcoming_trips.append(Trip(origin_city, destination_city))

    def update_city_info(self):
        self.update_temp()  # Update temperatures
        self.update_gas_prices()  # Update gas prices

    def update_gas_prices(self):
        # Randomly update gas prices for each city
        for city in self.cities:
            change = random.choice([-0.01, 0, 0.01])
            city.gas_prices += change  # Apply the change
            # Random chance to set this as the new base gas price
            if random.random() < 0.2:
                city.base_gas_prices = city.gas_prices

    def update_temp(self):
        # Update the temperature for each city based on current date
        for city in self.cities:
            # Normalize the date for temperature update
            temp_date = self.normalize_date(self.date)
            city.temp = random.gauss(
                city.get_temp(temp_date), 1
            )  # Update with some randomness

    def calculate_demand(self):
        # Process each trip to calculate demand and move completed trips to the completed list
        for trip in self.upcoming_trips:
            trip.calculate_demand()  # Calculate demand based on current trip parameters
        train_capacity = 300
        total_demand = sum(
            min(trip.demand, train_capacity) for trip in self.upcoming_trips
        )

        self.completed_trips.extend(self.upcoming_trips)
        self.upcoming_trips.clear()
        return total_demand

    def calculate_revenue(self):
        train_capacity = 300
        revenue = sum(
            min(trip.demand, train_capacity) * trip.price
            for trip in self.upcoming_trips
        )
        return revenue

    def score(self):
        # Calculate the total profit from all completed trips
        fixed_costs = 300
        passengers = self.calculate_demand()
        variable_costs = 0.3 * passengers
        revenue = self.calculate_revenue()

        profit = revenue - fixed_costs - variable_costs

        if profit > 0:
            return math.sqrt(profit) / len(self.completed_trips)
        return 0

    def update_prices(self, new_prices):
        # Update trip prices based on the action taken by the RL agent
        for i, new_price in enumerate(new_prices):
            if i < len(self.upcoming_trips):
                self.upcoming_trips[
                    i
                ].price = new_price  # Update the price of each trip

    def normalize_date(self, date):
        # Adjust the date for temperature updates, handling leap years
        if date.month == 2 and date.day == 29:
            return datetime.date(2022, 2, 28)
        return datetime.date(
            2022, date.month, date.day
        )  # Use 2022 as the base year for temperatures

    def get_city(self, name):
        # Retrieve a city object by its name
        return next((city for city in self.cities if city.name == name), None)

    def get_random_prices(self):
        min_price = 0
        max_price = 300
        return np.random.uniform(low=min_price, high=max_price, size=(10,)).astype(
            np.float32
        )
