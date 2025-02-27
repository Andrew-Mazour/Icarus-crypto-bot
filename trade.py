import requests
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig

def execute_trade(mint, public_key, private_key, rpc_endpoint):
    print(f"Attempting to trade for mint: {mint}")

    try:
        trade_response = requests.post(
            url="https://pumpportal.fun/api/trade-local",
            data={
                "publicKey": public_key,
                "action": "buy",
                "mint": mint,
                "amount": 100000,
                "denominatedInSol": "false",
                "slippage": 10,
                "priorityFee": 0.005,
                "pool": "pump"
            }
        )
        trade_response.raise_for_status()

        keypair = Keypair.from_base58_string(private_key)
        tx = VersionedTransaction(VersionedTransaction.from_bytes(trade_response.content).message, [keypair])
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)

        tx_payload = SendVersionedTransaction(tx, config)
        rpc_response = requests.post(
            url=rpc_endpoint,
            headers={"Content-Type": "application/json"},
            data=tx_payload.to_json()
        )
        # Handling response
        if rpc_response.status_code == 200 and 'result' in rpc_response.json():
            tx_signature = rpc_response.json()['result']
            print(f"Transaction successful: https://solscan.io/tx/{tx_signature}")
        else:
            print(f"RPC error: {rpc_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error executing trade: {e}")

def execute_sell(mint, public_key, private_key, rpc_endpoint):
    print(f"Attempting to sell for mint: {mint}")

    try:
        sell_response = requests.post(
            url="https://pumpportal.fun/api/trade-local",
            data={
                "publicKey": public_key,
                "action": "sell",
                "mint": mint,
                "amount": 100000,  # Adjust the amount as needed
                "denominatedInSol": "false",
                "slippage": 10,
                "priorityFee": 0.005,
                "pool": "pump"
            }
        )
        sell_response.raise_for_status()

        keypair = Keypair.from_base58_string(private_key)
        tx = VersionedTransaction(
            VersionedTransaction.from_bytes(trade_response.content).message,
            [keypair]
        )
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)

        tx_payload = SendVersionedTransaction(tx, config)
        rpc_response = requests.post(
            url=rpc_endpoint,
            headers={"Content-Type": "application/json"},
            data=tx_payload.to_json()
        )
        # Handling response
        if rpc_response.status_code == 200 and 'result' in rpc_response.json():
            tx_signature = rpc_response.json()['result']
            print(f"Sell transaction successful: https://solscan.io/tx/{tx_signature}")
        else:
            print(f"RPC error during sell: {rpc_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error executing sell trade: {e}")
