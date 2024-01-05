from env.env import CustomEnv
import random
import datetime
import numpy as np


def test_scores():
    env = CustomEnv()
    observation, info = env.reset()

    action = np.array(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7358346, 1.2508016, 0.0, 0.11548253],
        dtype=np.float32,
    )
    obs, reward, done, truncate, info = env.step(action)
    assert reward >= 0
    observation, info = env.reset()

    action = np.array(
        [
            10.0,
            10.0,
            220.0,
            110.0,
            220.0,
            110.0,
            220.7358346,
            123.22508016,
            240.0,
            103.11548253,
        ],
        dtype=np.float32,
    )

    obs, reward, done, truncate, info = env.step(action)
    assert reward >= 1

    action = np.array(
        [
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
            300.00,
        ],
        dtype=np.float32,
    )
    obs, reward, done, truncate, info = env.step(action)
    assert reward <= 100000


def test_observation_bounds():
    env = CustomEnv()
    observation, info = env.reset()
    assert env.observation_space.contains(
        observation
    ), "Reset observation out of bounds"

    for _ in range(10):  # Check a few steps
        action = env.action_space.sample()  # Random action
        observation, _, _, _, _ = env.step(action)
        assert env.observation_space.contains(
            observation
        ), "Step observation out of bounds"


def test_get_random_prices():
    e = CustomEnv()
    prices = e.get_random_prices()

    assert isinstance(prices, np.ndarray)
    assert prices.ndim == 1
    assert prices.shape == (10,)
    for i in prices:
        assert (
            i >= 0 and i <= 300
        ), "the random prices you're generating are not in [0,300]"

        assert isinstance(i, np.float32)

    # print(prices)


def test_env_flow():
    e = CustomEnv()
    assert len(e.upcoming_trips) == 0

    e.reset()
    assert len(e.upcoming_trips) == 10

    e.step(e.get_random_prices())
    assert len(e.upcoming_trips) == 10


def test_reset_function():
    e = CustomEnv()
    # Verify that reset output is not a tuple
    output = e.reset()
    # print(output.shape)
    assert isinstance(output, tuple) == True

    # Reset and get initial observation
    initial_observation, info = e.reset()

    # Check observation array structure
    assert initial_observation.ndim == 2
    assert initial_observation.shape == (
        10,
        6,
    )  # Assuming 10 trips with 6 features each
    assert isinstance(initial_observation, np.ndarray)

    # Check data types of elements in observation
    for i in range(initial_observation.shape[1]):
        assert initial_observation.dtype == np.float32

    # Verify observation is valid according to the observation space
    assert e.observation_space.contains(
        initial_observation
    ), "mismatch w/ observation space"

    # Ensure 10 upcoming trips are generated
    assert len(e.upcoming_trips) == 10

    # Integration check with Stable Baselines 3 (dummy check)
    try:
        from stable_baselines3 import PPO

        model = PPO("MlpPolicy", e, verbose=0)

        # print("Integration with Stable Baselines 3 successful.")
    except Exception as exc:
        print("Error during integration with Stable Baselines 3:", exc)
        assert False  # Force test to fail if there is an exception


def test_dimensionality_of_observation_space():
    # Assuming num_trips is defined
    num_trips = 10  # For example

    # Simulate an observation (This should come from your eironment)

    e = CustomEnv()
    obs, info = e.reset()

    # Check the shape
    expected_shape = (10, 6)
    assert (
        obs.shape == expected_shape
    ), f"Observation shape mismatch: Expected {expected_shape}, got {obs.shape}"


def test_calculate_demand():
    e = CustomEnv()
    e.reset()

    assert len(e.upcoming_trips) == 10
    e.update_prices([100, 200, 90, 80, 120, 300, 100, 50, 90, 110])  # simulating

    assert e.upcoming_trips[0].price != None

    e.update_city_info()

    e.calculate_demand()
    assert len(e.upcoming_trips) == 0


def test_generate_trips():
    e = CustomEnv()

    assert len(e.upcoming_trips) == 0
    e.reset()
    e.step(e.get_random_prices())
    assert len(e.upcoming_trips) == 10
    e.generate_trips(100)
    assert len(e.upcoming_trips) == 110


def test_step():
    e = CustomEnv()
    e.reset()

    action = e.get_random_prices()
    obs, reward, done, truncate, info = e.step(action)

    # print(obs)
    # print(reward)
    # print(done)


def test_trip_counts():
    e = CustomEnv()
    assert len(e.upcoming_trips) == 0

    # we create an env, and it has 0 trips added
    e.reset()
    assert len(e.upcoming_trips) == 10

    e.step(e.get_random_prices())
    assert len(e.upcoming_trips) == 10


def test_trip_data_format():
    e = CustomEnv()
    obs, info = e.reset()

    # Check the shape of the observation
    # This example assumes 10 trips with 6 features each; adjust according to your environment
    assert obs.shape == (10, 6), "Observation should have shape (10, 6)"

    # for feature in obs:
    #     print("Feature type: ", type(feature))

    assert isinstance(obs, np.ndarray), "Observation should be a numpy array"

    for i in range(len(obs)):
        assert isinstance(obs[i][0], np.float32)
        assert isinstance(obs[i][1], np.float32)
        assert isinstance(obs[i][2], np.float32)
        assert isinstance(obs[i][3], np.float32)
        assert isinstance(obs[i][4], np.float32)
        assert isinstance(obs[i][5], np.float32)

    for i in range(len(obs)):
        assert obs[i][0] >= 0, "check first obs col"
        assert obs[i][1] >= 0, "check 2nd obs col"
        assert obs[i][2] >= 0, "check 3rd col"
        assert obs[i][3] >= 0, "check 4th col"
        assert obs[i][4] >= -30, "check 5th col"
        assert obs[i][5] >= -30, "check 6th col"
