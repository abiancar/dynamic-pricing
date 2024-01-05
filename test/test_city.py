from city.city import City


def test_city_creation():
    philly = City(name="Philadelphia", pop=600000, ue_rate=0.10, gas=3.00, id=3)

    assert philly.pop == 600000
    assert philly.name == "Philadelphia"
    assert philly.ue_rate == 0.1
    assert philly.base_gas_prices == 3
    assert philly.id == 3
