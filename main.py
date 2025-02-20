import asyncio
import json
from utils import extract_mint, record_trade_time, custom_sell_condition
from trade import execute_trade, execute_sell
from config import RATE_OF_CHANGE_THRESHOLD, TIME_WINDOW
import websockets
from utils import coins

coins_populated_event = asyncio.Event()

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        payload = {"method": "subscribeNewToken"}
        await websocket.send(json.dumps(payload))

        async for message in websocket:
            extract_mint(json.loads(message))

async def token(public_key, private_key, rpc_endpoint):
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        await coins_populated_event.wait()

        payload = {
            "method": "subscribeTokenTrade",
            "keys": coins[0]
        }
        await websocket.send(json.dumps(payload))

        async for message in websocket:
            message_json = json.loads(message)
            if 'marketCapSol' in message_json and 'mint' in message_json:
                record_trade_time(message_json['mint'])
                print(f"Trade: {message_json['mint']} market cap: {message_json['marketCapSol']}")

                # Buy logic based on market cap
                if 35 <= message_json['marketCapSol'] <= 60:
                    print(message_json['mint'])
                    print("!!! BUY !!!")
                    await execute_trade(message_json['mint'], public_key, private_key, rpc_endpoint)

                # Sell logic if market cap exceeds 70
                if message_json['marketCapSol'] > 70:
                    print(message_json['mint'])
                    print("!!! SELL (Market cap exceeded 70) !!!")
                    await execute_sell(message_json['mint'], public_key, private_key, rpc_endpoint)

                # Sell logic for rapid market cap decrease
                if custom_sell_condition(message_json):
                    print(message_json['mint'])
                    print("!!! SELL (Rapid Market Cap Drop) !!!")
                    await execute_sell(message_json['mint'], public_key, private_key, rpc_endpoint)

async def main():
    public_key = "your_public_key"
    private_key = "your_private_key"
    rpc_endpoint = "https://api.mainnet-beta.solana.com"

    subscribe_task = asyncio.create_task(subscribe())
    token_task = asyncio.create_task(token(public_key, private_key, rpc_endpoint))
    await asyncio.gather(subscribe_task, token_task)

asyncio.run(main())
