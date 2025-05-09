import random
import pandas as pd
from datetime import datetime, timedelta

def generate_withdrawal_queries(contracts_csv, users_csv):
    # Load contracts and users data
    contracts_df = pd.read_csv(contracts_csv, dtype=str)
    users_df = pd.read_csv(users_csv, dtype=str)

    withdrawal_queries = []
    reasons = [
        "Payment issues and disputes.",
        "Freelancer unable to complete the project.",
        "Client requested project cancellation.",
        "Scope of work changed significantly.",
        "Mutual agreement to terminate contract."
    ]

    # Process cancelled contracts (majority of the data)
    cancelled_contracts = contracts_df[contracts_df["status"] == "cancelled"]
    for _, contract in cancelled_contracts.iterrows():
        contract_id = contract["contract_id"]
        freelancer_id = contract["freelancer_id"]
        client_id = contract["client_id"]

        # Randomly assign who requested (either freelancer or client)
        requested_by = random.choice([freelancer_id, client_id])
        approved_by = client_id if requested_by == freelancer_id else freelancer_id  # Opposite party approves

        status = random.choice(["approved", "rejected"])  # Random decision for cancelled contracts
        reason = random.choice(reasons)

        withdrawn_at = (datetime.today() - timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d %H:%M:%S')

        withdrawal_queries.append(
            f"INSERT INTO withdrawals (requested_by, approved_by, contract_id, reason, status, withdrawn_at) "
            f"VALUES ('{requested_by}', '{approved_by}', '{contract_id}', '{reason}', '{status}', '{withdrawn_at}');"
        )

    # Process active contracts (add a few `pending` requests)
    active_contracts = contracts_df[contracts_df["status"] == "active"].sample(n=min(5, len(contracts_df)))
    for _, contract in active_contracts.iterrows():
        contract_id = contract["contract_id"]
        freelancer_id = contract["freelancer_id"]
        client_id = contract["client_id"]

        requested_by = random.choice([freelancer_id, client_id])  # Random requester
        approved_by = client_id if requested_by == freelancer_id else freelancer_id  # Opposite party
        reason = random.choice(reasons)

        # Pending requests for active contracts
        withdrawal_queries.append(
            f"INSERT INTO withdrawals (requested_by, approved_by, contract_id, reason, status) "
            f"VALUES ('{requested_by}', '{approved_by}', '{contract_id}', '{reason}', 'pending');"
        )

    # Save queries to a file
    with open("insert_withdrawals.sql", "w") as f:
        f.write("\n".join(withdrawal_queries))

    print(f"SQL file generated successfully: insert_withdrawals.sql ({len(withdrawal_queries)} withdrawals)")

# Example Usage:
generate_withdrawal_queries("withdrawals/contracts.csv", "withdrawals/users.csv")
