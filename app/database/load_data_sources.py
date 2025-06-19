from sqlalchemy import create_engine
import pandas as pd
import numpy as np
    
def load_dummy_loan_dataframes() -> dict[str, pd.DataFrame]:
    # Customers with realistic attributes
    customers = {
        "customer_id": range(1, 101),
        "name": [f"Customer_{i}" for i in range(1, 101)],
        "kyc_status": np.random.choice(["verified", "pending", "rejected"], 100, p=[0.7, 0.2, 0.1]),
        "age": np.random.randint(18, 70, 100),
        "join_date": pd.date_range('2022-01-01', periods=100, freq='D').tolist(),
        "region": np.random.choice(["North", "South", "East", "West"], 100)
    }
    
    # Accounts with balances
    accounts = {
        "customer_id": np.random.choice(range(1, 101), 1000),
        "account_id": [f"ACC{1000+i}" for i in range(1000)],
        "balance": np.round(np.random.uniform(100, 10000, 1000), 2),
        "account_type": np.random.choice(["Savings", "Current", "Business"], 1000, p=[0.6, 0.3, 0.1])
    }
    
    # Transactions with temporal patterns
    transactions = {
        "transaction_id": range(1, 5001),
        "account_id": np.random.choice(accounts["account_id"], 5000),
        "to_account": np.random.choice(accounts["account_id"], 5000),
        "amount": np.round(np.abs(np.random.normal(500, 300, 5000)), 2),
        "fee": lambda x: np.round(x * 0.01 + 0.5, 2),
        "datetime": pd.date_range('2023-01-01', periods=5000, freq='T').tolist(),
        "transaction_type": np.random.choice(
            ["deposit", "transfer", "withdrawal", "bill_payment"], 
            5000,
            p=[0.3, 0.4, 0.2, 0.1]
        ),
        "merchant_category": np.random.choice(
            ["Retail", "Food", "Utilities", "Transport", "Other"],
            5000
        )
    }
    transactions["fee"] = transactions["fee"](transactions["amount"])
    transactions["net_impact"] = transactions["amount"] - transactions["fee"]
    
    return {
        "customers": pd.DataFrame(customers),
        "accounts": pd.DataFrame(accounts),
        "transactions": pd.DataFrame(transactions),
    }