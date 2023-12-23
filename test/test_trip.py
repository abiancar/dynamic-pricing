from city.city import City
from trip.trip import Trip
from env.env import Env
import datetime


env = Env()


def test_trip_creation():
    t = Trip(env.get_city("Philadelphia"), env.get_city("Baltimore"))
    assert t.departure_time != datetime.datetime.now()
    assert t.origin.name == "Philadelphia"
    assert t.destination.name == "Baltimore"
    assert t.car_distance == 106


def test_trip_with_env_step():
    e = Env()
    t = Trip(env.get_city("Boston"), env.get_city("Washington DC"))

    e.upcoming_trips.append(t)

    for i in range(100):
        e.step()
        print(t.calculate_demand)
