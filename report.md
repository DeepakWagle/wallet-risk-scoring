# 📊 Compound Wallet Risk Scoring - Stage 2

## ✅ Data Collection

- Fetched on-chain transaction history using **Covalent API** for 103 wallets.
- API Key used: `cqt_rQDkrvqrTTqWgdFW6fmXtJQ6GrWX`
- Queried transactions across **Compound V2** protocol.
- Raw JSON responses saved under `data/raw_txn_data/`.

---

## 🛠 Feature Engineering

For each wallet, extracted:
- `num_tx`: Number of transactions
- `total_amount`: Total value transacted
- `avg_tx_amount`: Average transaction value
- `num_mint`: Mint operations (deposit)
- `num_redeem`: Withdraw operations
- `num_borrow`: Borrow activity
- `num_repay`: Repayment activity

Stored in: `data/wallet_features.csv`

---

## 📈 Risk Scoring Logic

1. **Normalization**: Applied `MinMaxScaler` to scale features between 0–1.
2. **Weighting**:
   - `num_tx`, `total_amount`, `avg_tx_amount`, `num_repay`: Positive indicators
   - Absence of activity resulted in lower scores
3. **Final Score**: Scaled to range 0–1000

Higher score → Active, repayment-heavy, trustworthy  
Lower score → Inactive or suspicious behavior

---

## 📊 Visualization

- Distribution of final risk scores shown in `assets/risk_score_distribution.png`

---

## 📁 Deliverables

- ✅ `wallet_score.csv`  
- ✅ Feature script: `src/feature_engineering.py`  
- ✅ Raw data folder: `data/raw_txn_data/`  
- ✅ Visualization asset: `assets/risk_score_distribution.png`

---

## 🚀 Conclusion

This model offers a scalable way to assess the risk of DeFi wallets using on-chain activity on Compound V2. The pipeline can be extended to more wallets or protocols (e.g., Aave, Uniswap).
