import random
import pandas as pd
from datetime import datetime, timedelta

def generate_invoice_queries(contracts_csv, payments_csv):
    # Load contracts and payments data
    contracts_df = pd.read_csv(contracts_csv, dtype=str)
    payments_df = pd.read_csv(payments_csv, dtype=str)

    invoice_queries = []

    # Process active and completed contracts
    for _, contract in contracts_df.iterrows():
        contract_id = contract["contract_id"]
        agreed_price = float(contract["agreed_price"])
        contract_status = contract["status"]

        # Invoice net amount is the agreed price
        net_amount = round(agreed_price, 2)

        # Generate due date within 30 days of today
        due_date = (datetime.today() + timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')

        # Check if a completed payment exists for this contract
        payment_made = payments_df[(payments_df["contract_id"] == contract_id) & (payments_df["status"] == "completed")]

        # Determine invoice status based on contract status and payment
        if contract_status == "completed" and not payment_made.empty:
            status = "paid"
            paid_at = f"'{(datetime.today() - timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d')}'"
        elif contract_status == "completed" and payment_made.empty:
            status = "overdue"
            paid_at = "NULL"
        else:
            status = "pending"
            paid_at = "NULL"

        invoice_queries.append(
            f"INSERT INTO invoices (contract_id, net_amount, due_date, status, paid_at) "
            f"VALUES ('{contract_id}', {net_amount}, '{due_date}', '{status}', {paid_at});"
        )

    # Save queries to file
    with open("insert_invoices.sql", "w") as f:
        f.write("\n".join(invoice_queries))

    print(f"SQL file generated successfully: insert_invoices.sql ({len(invoice_queries)} invoices)")

# Example Usage:
generate_invoice_queries("payments&invoices/contracts.csv", "payments&invoices/payments.csv")
