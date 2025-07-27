import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os

INPUT_FILE = "data/wallet_features.csv"
OUTPUT_FILE = "wallet_score.csv"
PLOT_FILE = "assets/risk_score_distribution.png"

def main():
    # Load data
    df = pd.read_csv(INPUT_FILE)
    df.fillna(0, inplace=True)

    # Features to consider for scoring
    features = ['num_tx', 'total_amount', 'avg_tx_amount',
                'num_mint', 'num_redeem', 'num_borrow', 'num_repay']
    X = df[features]

    # Normalize using MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Weighted scoring logic (can be tuned)
    weights = np.array([0.2, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1])
    raw_scores = np.dot(X_scaled, weights)

    # Scale to 0–1000
    final_scores = (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min()) * 1000

    # Save to CSV
    os.makedirs("assets", exist_ok=True)
    output_df = pd.DataFrame({
        'wallet_id': df['wallet'],
        'score': final_scores.round().astype(int)
    })
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Risk scores saved to: {OUTPUT_FILE}")

    # Plot score distribution
    plt.figure(figsize=(8, 5))
    plt.hist(output_df['score'], bins=20, edgecolor='black')
    plt.title("Wallet Risk Score Distribution")
    plt.xlabel("Score (0–1000)")
    plt.ylabel("Wallet Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    print(f"📊 Distribution plot saved to: {PLOT_FILE}")

if __name__ == "__main__":
    main()
