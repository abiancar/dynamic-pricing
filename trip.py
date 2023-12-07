import datetime
from city import City
import random
import math

distances = {
    "Baltimore": {
        "Washington DC": 41,
        "Philadelphia": 106,
        "Boston": 404,
        "New York City": 191,
    },
    "Washington DC": {
        "Baltimore": 41,
        "Philadelphia": 142,
        "Boston": 443,
        "New York City": 229,
    },
    "Philadelphia": {
        "Baltimore": 106,
        "Washington DC": 142,
        "Boston": 308,
        "New York City": 97,
    },
    "Boston": {
        "Baltimore": 404,
        "Washington DC": 443,
        "Philadelphia": 308,
        "New York City": 215,  # This value is based on an average of common distances found online.
    },
    "New York City": {
        "Baltimore": 191,
        "Washington DC": 229,
        "Philadelphia": 97,
        "Boston": 215,
    },
}


class Trip:
    def __init__(self, origin: City, destination: City, departure_time=None):
        self.origin = origin
        self.destination = destination
        self.departure_time = (
            departure_time if departure_time else self.get_random_time()
        )

        self.average_cost = 150
        self.demand = 0
        self.car_distance = distances[self.origin.name][self.destination.name]

    def get_random_time(self):
        curr = datetime.datetime.now()
        curr_y = curr.year
        curr_m = curr.month
        curr_d = curr.day
        curr_h = curr.hour

        random_hr = random.randint(curr_h, 23)
        random_min = random.randint(0, 59)

        return datetime.datetime(curr_y, curr_m, curr_d, random_hr, random_min)

    # more demand during business hours
    def calc_hour_modifier(self):
        # Assuming self.departure_time is a datetime object
        # Check if it's a weekday
        if self.departure_time.weekday() < 5:  # Monday is 0, Sunday is 6
            # Peak business hours
            if 8 <= self.departure_time.hour < 17:
                return 1.0  # No modification needed
            else:
                # Decrease demand as it gets later
                return 0.5  # Example: 50% of base demand
        else:
            # Weekends have different peak hours
            if 10 <= self.departure_time.hour < 20:
                return 1.0
            else:
                return 0.5  # Example: 50% of base demand

    def calculate_weather_modifier(self):
        # Calculate the average temperature
        avg_temp = (self.origin.temp + self.destination.temp) / 2
        # Determine the deviation from the ideal temperature
        deviation = abs(avg_temp - 68)
        # Apply the deviation in a non-linear fashion, with no penalty within a comfortable range
        weather_modifier = 1 - (
            0.005 * deviation if deviation > 5 else 0
        )  # No penalty for +/- 5 degrees from ideal
        return weather_modifier

    def calculate_price_modifier(self):
        # Assuming that prices above 100 decrease demand and below 100 increase demand
        price_difference = self.average_cost - 100
        # Apply a softer, bounded exponential curve instead of a cubic
        price_modifier = (
            math.exp(-0.05 * price_difference)
            if price_difference > 0
            else 1 + 0.05 * price_difference
        )
        return price_modifier

    def unemployment_demand_modifier(self):
        """
        Calculate the demand modifier based on the unemployment rate.

        :param unemployment_rate: The unemployment rate of the city as a decimal (e.g., 0.10 for 10%)
        :return: The demand modifier as a decimal (e.g., 0.90 for a -10% modifier)
        """

        def ue_modifier(unemployment_rate):
            # Define the baseline unemployment rate where there is no impact on demand
            baseline_ue_rate = 0.05  # e.g., 5% unemployment is considered 'normal'

            # Define the impact rate, which determines how much the demand changes per percentage point change in unemployment
            impact_rate = (
                0.02  # e.g., each 1% above the baseline decreases demand by 2%
            )

            # Calculate the modifier
            if unemployment_rate <= baseline_ue_rate:
                # If the unemployment rate is at or below the baseline, there's no negative effect on demand
                modifier = 1.0
            else:
                # If the unemployment rate is above the baseline, reduce demand proportionally
                modifier = 1 - (unemployment_rate - baseline_ue_rate) * impact_rate

            # Ensure the modifier does not increase demand above 100% or reduce it below a certain threshold, say 50%
            modifier = max(0.5, min(1, modifier))
            return modifier

        origin_modifier = ue_modifier(self.origin.ue_rate)
        destination_modifier = ue_modifier(self.destination.ue_rate)

        return (origin_modifier + destination_modifier) / 2

    def calculate_gas_modifier(self):
        # Logarithmic adjustment, where the effect of gas prices plateaus at a certain point.

        # average car gets 36 miles per gallon

        # cost per gallon * number of gallons
        driving_cost = self.origin.gas_prices * self.car_distance / 36
        driving_cost_difference = driving_cost - self.average_cost

        print(driving_cost_difference)
        return (
            0
            if driving_cost_difference == 0
            else -2 * math.log1p(driving_cost_difference)
            if driving_cost_difference > 0
            else 2 * math.log1p(-1 * driving_cost_difference)
        )

    def calculate_demand(self):
        # Assuming the pops are large, we can take a much smaller percentage
        base_demand = (
            self.origin.pop * self.destination.pop
        ) ** 0.5  # Square root as an example

        """modifiers"""
        # Ensure modifiers are between 0 and 1
        gas_modifier = self.calculate_gas_modifier()
        unemployment_modifier = self.unemployment_demand_modifier()
        weather_modifier = self.calculate_weather_modifier()
        datetime_modifier = self.calc_hour_modifier()
        price_modifier = self.calculate_price_modifier()

        # Apply modifiers using a product, ensuring none of them can exceed a multiplier of 1
        demand = (
            base_demand
            * gas_modifier
            * unemployment_modifier
            * weather_modifier
            * datetime_modifier
            * price_modifier
        )

        # Introduce elasticity (for example, price elasticity)
        elasticity = (
            -0.15
        )  # This is an example value; it would need to be empirically determined
        demand *= 1 + elasticity * (self.average_cost - 100)

        # Cap the demand to the lower of the two city pops
        max_demand = min(self.origin.pop, self.destination.pop)
        demand = min(demand, max_demand)
        self.demand = max(0, demand)
        return self.demand

    def __str__(self):
        return f"{self.origin.name} --> {self.destination.name} at {self.departure_time}. Demand: {round(self.demand)} interested riders @ ${round(self.average_cost, 2)}"
