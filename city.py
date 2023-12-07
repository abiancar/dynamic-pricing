import random


class City:
    def __init__(self, name, pop, temp, ue_rate, gas):
        self.name = name
        self.pop = pop
        self.base_temp = temp
        self.temp = temp
        self.ue_rate = ue_rate
        self.base_gas_prices = gas
        self.gas_prices = gas

    def update_gas_prices(self):
        outcome = random.choice([-0.01, 0, 0.01])
        self.gas_prices += outcome
        # there is 1% chance that this gas price will become the new 'base'
        if random.randint(0, 100) == 52:
            self.base_gas_prices = self.gas_prices
