from city.city import City
from trip.trip import Trip
from env.env import CustomEnv
import datetime


def test_trip_creation():
    e = CustomEnv()
    e.reset()
    t = Trip(e.get_city("Philadelphia"), e.get_city("Baltimore"))
    assert t.departure_time != datetime.datetime.now()
    assert t.origin.name == "Philadelphia"
    assert t.destination.name == "Baltimore"
    assert t.car_distance == 106


def test_trip_generation():
    e = CustomEnv()
    e.reset()
    e.generate_trips(100)
    assert len(e.upcoming_trips) == 110


def test_trip_demand_modifiers():
    e = CustomEnv()
    e.reset()
    e.generate_trips(1)

    t = e.upcoming_trips[0]
    t.price = 100

    assert t.calculate_gas_modifier() != 0
    assert t.unemployment_demand_modifier() != 0
    assert t.calculate_weather_modifier() != 0
    assert t.calculate_hour_modifier() != 0
    assert t.calculate_price_modifier() != 0
    assert t.calculate_demand() != 0
    # print("base demand: ", t.get_base_demand())
    # print("origin gas price: ", t.origin.gas_prices)
    # print("destination gas price: ", t.destination.gas_prices)
    # print("train - car price:", t.calculate_train_minus_car())
    # print("ticket price: $", t.average_cost)
    # print("modifier: gas", t.calculate_gas_modifier())
    # print("modifier: ue", t.unemployment_demand_modifier())
    # print("modifier: weather", t.calculate_weather_modifier())
    # print("modifier: hour", t.calculate_hour_modifier())
    # print("modifier: price", t.calculate_price_modifier())
    # print("modifier: demand", t.calculate_demand())
