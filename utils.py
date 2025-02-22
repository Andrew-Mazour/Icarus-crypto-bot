import time
from config import RATE_OF_CHANGE_THRESHOLD, TIME_WINDOW
import asyncio

coins = [[], []]
coins_populated_event = asyncio.Event()
market_cap_history = {}

def record_trade_time(mint):
    if mint in coins[0]:
        index = coins[0].index(mint)
        coins[1][index] = time.time()  # Update the trade time
    else:
        pass

def extract_mint(message):
    current_time = time.time()
    if 'marketCapSol' in message and message['marketCapSol'] < 45:
        if len(coins[0]) <= 20:
            coins[0].append(message['mint'])
            coins[1].append(current_time)
            coins_populated_event.set()
            print(f"New mint added: {message['mint']}")
        elif all(current_time - trade_time >= 180 for trade_time in coins[1]):
            oldest_trade_index = coins[1].index(min(coins[1]))
            coins[0].pop(oldest_trade_index)
            coins[1].pop(oldest_trade_index)
        else:
            pass
    else:
        print("Market cap too high")

def custom_sell_condition(message):
    mint = message['mint']
    current_time = time.time()

    if 'marketCapSol' in message:
        current_market_cap = message['marketCapSol']

        # If this is the first time we are seeing this token, we store its market cap and timestamp
        if mint not in market_cap_history:
            market_cap_history[mint] = {'market_cap': current_market_cap, 'timestamp': current_time}
            return False  # No decision yet

        # Get the previous market cap and timestamp
        previous_market_cap = market_cap_history[mint]['market_cap']
        previous_timestamp = market_cap_history[mint]['timestamp']

        # If the time difference is within the window, calculate the rate of change
        if current_time - previous_timestamp <= TIME_WINDOW:
            market_cap_change = ((previous_market_cap - current_market_cap) / previous_market_cap) * 100
            if market_cap_change >= RATE_OF_CHANGE_THRESHOLD:
                print(f"Market cap decreased by {market_cap_change:.2f}% for mint {mint}. Selling!")
                return True  # Sell if the decrease is rapid
        else:
            # Update the stored data if the time window has passed
            market_cap_history[mint] = {'market_cap': current_market_cap, 'timestamp': current_time}

    return False  # Default is to not sell
