import random
import pandas as pd

def generate_payment_queries(contracts_csv):
    # Load contracts data
    contracts_df = pd.read_csv(contracts_csv, dtype=str)

    payment_methods = ["Credit Card", "Bank Transfer", "PayPal", "Cryptocurrency"]
    payment_queries = []

    # Process only completed contracts
    completed_contracts = contracts_df[contracts_df["status"] == "completed"]

    for _, contract in completed_contracts.iterrows():
        contract_id = contract["contract_id"]
        agreed_price = float(contract["agreed_price"])

        # Assign payment amount (full or partial)
        amount = round(random.uniform(agreed_price * 0.8, agreed_price), 2)  # Between 80%-100% of agreed price
        payment_method = random.choice(payment_methods)
        status = random.choice(["completed", "failed"])

        payment_queries.append(
            f"INSERT INTO payments (contract_id, amount, payment_method, status) "
            f"VALUES ('{contract_id}', {amount}, '{payment_method}', '{status}');"
        )

    # Save queries to file
    with open("insert_payments.sql", "w") as f:
        f.write("\n".join(payment_queries))

    print(f"SQL file generated successfully: insert_payments.sql ({len(payment_queries)} payments)")

# Example Usage:
generate_payment_queries("payments&invoices/contracts.csv")
