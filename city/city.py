import random
import pandas as pd


class City:
    def __init__(self, name, pop, ue_rate, gas):
        self.name = name
        self.pop = pop
        self.temp = 0
        self.ue_rate = ue_rate
        self.base_gas_prices = gas
        self.gas_prices = gas

    def update_gas_prices(self):
        outcome = random.choice([-0.01, 0, 0.01])
        self.gas_prices += outcome
        # there is 1% chance that this gas price will become the new 'base'
        if random.randint(0, 100) == 52:
            self.base_gas_prices = self.gas_prices

    def get_temp(self, date):
        city_file_name = self.name.lower().replace(" ", "_")
        weather = pd.read_csv(f"./.weather_data/{city_file_name}_weather.csv")

        # Convert the 'time' column to datetime and then extract the date part
        weather["time"] = pd.to_datetime(weather["time"]).dt.date

        # Set the 'time' column as the index
        weather.set_index("time", inplace=True)

        # Ensure the DataFrame index is sorted
        weather.sort_index(inplace=True)
        return weather.loc[date]["tavg"]
