import math


price = 0
ideal_price = 100

for i in range(300):
    # Assuming that prices above 100 decrease demand and below 100 increase demand
    price_difference = price - ideal_price
    # Apply a softer, bounded exponential curve instead of a cubic

    price_modifier = math.exp(-0.05 * price_difference)
    if price <= ideal_price:
        price_modifier = abs(math.exp(-0.05 * price_difference))

    price += 1
    # print(f"price_modifier: {price_modifier}, for price: {price}")

    print(min(price_modifier * 800, 300) * price, price)
