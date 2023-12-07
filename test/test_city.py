from city import City


def test_city_creation():
    philly = City(name="Philadelphia", pop=60000, temp=70, ue_rate=0.10, gas=3.00)

    assert philly.pop == 60000
    assert philly.name == "Philadelphia"
    assert philly.temp == 70
    assert philly.ue_rate == 0.1
    assert philly.base_gas_prices == 3


def test_city_update_gas_prices():
    philly = City(name="Philadelphia", pop=60000, temp=70, ue_rate=0.10, gas=3.00)

    assert philly.base_gas_prices == 3

    for i in range(10000):
        philly.update_gas_prices()
        # print(philly.gas_prices)

    change = (philly.gas_prices - philly.base_gas_prices) / philly.base_gas_prices * 100
    print(f"gas prices moved {'down' if change >= 0 else 'down' } by {round(change)} %")
    assert philly.gas_prices != 3
