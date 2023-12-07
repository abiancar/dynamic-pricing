from city import City
from trip import Trip
import datetime


philadelphia = City("Philadelphia", 1527886, temp=70, ue_rate=0.1, gas=3.5)
nyc = City("New York City", 7888121, temp=67, ue_rate=0.05, gas=5)
washington = City("Washington DC", 631693, temp=72, ue_rate=0.07, gas=4)
baltimore = City("Baltimore", 563455, temp=69, ue_rate=0.024, gas=3.37)
boston = City("Boston", 654776, temp=50, ue_rate=0.006, gas=5)

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


def test_trip_creation():
    t = Trip(baltimore, boston)
    assert t.departure_time != datetime.datetime.now()
    assert t.origin.name == "Baltimore"
    assert t.destination.name == "Boston"
    assert t.car_distance == 404


from env import Env
from city import City
from trip import Trip

philadelphia = City("Philadelphia", 1527886, temp=70, ue_rate=0.1, gas=3.5)
nyc = City("New York City", 7888121, temp=67, ue_rate=0.05, gas=5)
washington = City("Washington DC", 631693, temp=72, ue_rate=0.07, gas=4)
baltimore = City("Baltimore", 563455, temp=69, ue_rate=0.024, gas=3.37)
boston = City("Boston", 654776, temp=50, ue_rate=0.006, gas=5)
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


def test_trip_with_env_step():
    e = Env()
    t = Trip(boston, washington)

    e.upcoming_trips.append(t)

    for i in range(100):
        e.step()
        print(t.calculate_demand)
