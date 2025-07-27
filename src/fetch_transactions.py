# src/fetch_transactions.py

import requests
import pandas as pd
import os
import time
import json


COVALENT_API_KEY = "cqt_rQDkrvqrTTqWgdFW6fmXtJQ6GrWX"
CHAIN_ID = 1  # Ethereum mainnet

def fetch_compound_transactions(wallet_address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v2/"
    params = {
        "key": COVALENT_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[!] Failed for {wallet_address}: {response.status_code}")
        return None

def main():
    os.makedirs("data/raw_txn_data", exist_ok=True)
    
    wallets = pd.read_csv("data/wallets.csv")  # Ensure column is named 'wallet'
    for i, row in wallets.iterrows():
        wallet = row['wallet_id'].strip()
        print(f"[{i+1}/{len(wallets)}] Fetching: {wallet}")
        result = fetch_compound_transactions(wallet)
        if result:
            with open(f"data/raw_txn_data/{wallet}.json", "w") as f:
                f.write(json.dumps(result))
        time.sleep(1.2)  # Respect API rate limits

if __name__ == "__main__":
    main()
