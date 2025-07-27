import os
import json
import pandas as pd
from tqdm import tqdm

RAW_DIR = "data/raw_txn_data"
FEATURED_CSV = "data/wallet_features.csv"

def parse_transactions(filepath):
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None  # skip corrupted files

    wallet_address = os.path.basename(filepath).replace(".json", "")
    transactions = data.get("data", {}).get("items", [])

    if not transactions:
        return None

    features = {
        "wallet": wallet_address,
        "num_tx": len(transactions),
        "total_amount": 0,
        "avg_tx_amount": 0,
        "num_mint": 0,
        "num_redeem": 0,
        "num_borrow": 0,
        "num_repay": 0,
    }

    amounts = []
    for txn in transactions:
        try:
            amount = float(txn.get("value", 0))  # or use 'amount' if it's under a different key
            amounts.append(amount)
        except (ValueError, TypeError):
            continue

        tx_type = txn.get("decoded", {}).get("name", "").lower()
        if "mint" in tx_type:
            features["num_mint"] += 1
        elif "redeem" in tx_type:
            features["num_redeem"] += 1
        elif "borrow" in tx_type:
            features["num_borrow"] += 1
        elif "repay" in tx_type:
            features["num_repay"] += 1

    features["total_amount"] = sum(amounts)
    features["avg_tx_amount"] = sum(amounts) / len(amounts) if amounts else 0

    return features

def main():
    rows = []
    for file in tqdm(os.listdir(RAW_DIR)):
        filepath = os.path.join(RAW_DIR, file)
        if not filepath.endswith(".json"):
            continue

        row = parse_transactions(filepath)
        if row:
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(FEATURED_CSV, index=False)
    print(f"\n✅ Feature extraction complete. Saved to {FEATURED_CSV}")

if __name__ == "__main__":
    main()
