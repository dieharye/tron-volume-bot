import time
import random
import os
import subprocess
import tkinter as tk
import threading
import getpass
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from tronpy.exceptions import TransactionError, AddressNotFound, TransactionNotFound
from dotenv import load_dotenv
from decimal import Decimal, ROUND_DOWN
import requests
import traceback

print("Discover more scripts at solana-scripts.com")
print('https://t.me/benorizz0')

time.sleep(3)

print("Tron Volume Bot - @benorizz0")

time.sleep(2)


node_url = os.getenv("NODE_API_KEY")
main_wallet_address = os.getenv("MAIN_WALLET_ADDRESS")
main_wallet_private_key = os.getenv("MAIN_WALLET_PRIVATE_KEY")
num_wallets = int(os.getenv("NUM_WALLETS", 1))
trade_delay = int(os.getenv("TRADE_DELAY", 1))
min_trade_amount = float(os.getenv("MIN_TRADE_AMOUNT", 0.1))
max_trade_amount = float(os.getenv("MAX_TRADE_AMOUNT", 1.0))
target_token_address = os.getenv("TARGET_TOKEN_ADDRESS")


# Example: Get the balance of the main wallet address
balance = client.get_account_balance(main_wallet_address)
print(f"Balance of main wallet: {balance} TRX")

# Main wallet details
main_wallet = {
    "address": main_wallet_address,
    "private_key": PrivateKey(bytes.fromhex(main_wallet_private_key))
}

# Wallet creation function
def create_wallets(n):
    wallets = []
    for i in range(n):
        private_key = PrivateKey.random()
        wallet_info = {
            "name": f"Wallet{i+1}",
            "address": private_key.public_key.to_base58check_address(),
            "private_key": private_key.hex()
        }
        wallets.append(wallet_info)
    return wallets

# Function to find the next available filename
def get_next_filename(base_name='wallets', extension='txt'):
    i = 1
    while True:
        file_name = f"{base_name}{i}.{extension}"
        if not os.path.exists(file_name):
            return file_name
        i += 1

# Save wallets to a uniquely named file
def save_wallets_to_file(wallets):
    file_path = get_next_filename()
    with open(file_path, 'w') as f:
        for wallet in wallets:
            f.write(f"Name: {wallet['name']}\n")
            f.write(f"Address: {wallet['address']}\n")
            f.write(f"Private Key: {wallet['private_key']}\n\n")
    print(f"Wallets saved to {file_path}")

# Function to distribute TRX from main wallet to other wallets
def distribute_trx_and_swap(main_wallet, wallets):
    # Get total balance as a Decimal object
    total_balance = Decimal(client.get_account_balance(main_wallet["address"]))
    num_wallets = len(wallets)

    time.sleep(1)

    # Estimate the fee for each transaction (typically 1 TRX)
    estimated_fee_per_tx_sun = 1_000_000  # 1 TRX in Sun
    total_estimated_fee_sun = estimated_fee_per_tx_sun * num_wallets
    # Wait for the approval transaction to be confirmed
    print("Waiting for token approval...")
    client.wait_for_transaction_receipt(approve_tx['txid'])

    # Set the swap path (token -> TRX)
    path = [
        client.to_base58check_address(contract_address),  # Token address
        client.to_base58check_address(client.TRX_CONTRACT_ADDRESS)  # TRX address
    ]

    # Create the swap transaction
    print("Creating swap transaction...")
    swap_tx = (
        token_contract.functions.swapExactTokensForTRX(
            amount_to_swap_sun,
            0,  # Minimum output amount (can be used to set slippage)
            path,
            wallet_address,
            int(client.get_latest_block()['block_header']['raw_data']['timestamp']) + 1200  # 20 minutes deadline
        )
        .with_owner(wallet_address)
        .fee_limit(2_000_000)
        .build()
        .sign(priv_key)
    )

    # Send the transaction
    print("Sending the transaction...")
    tx_hash = client.broadcast(swap_tx)
    print(f"Transaction sent! Transaction Hash: {tx_hash}")

    # Call the function
    swap_tokens_for_trx()

# Trade function
def trade_wallets(wallets):
    for wallet in wallets:
        if stop_event.is_set():
            print("STOP button pressed. Exiting trading loop.")
            return

        trade_amount = round(random.uniform(min_trade_amount, max_trade_amount), 6)
        send_transaction(wallet, trade_amount, is_purchase=True)  # Purchase
        time.sleep(trade_delay)

        if sell_after_purchase:
            send_transaction(wallet, trade_amount, is_purchase=False)  # Sale
            time.sleep(trade_delay)

distribute_trx_and_swap(main_wallet, wallets)
trade_wallets(wallets)