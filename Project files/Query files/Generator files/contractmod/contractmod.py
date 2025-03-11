import random
import pandas as pd
from datetime import datetime, timedelta

def generate_contract_modification_queries(contracts_csv, users_csv):
    # Load contracts and users data
    contracts_df = pd.read_csv(contracts_csv, dtype=str)  # Read everything as a string
    users_df = pd.read_csv(users_csv, dtype=str)

    modification_queries = []

    # Select a subset of contracts for modifications
    modified_contracts = contracts_df.sample(frac=0.4)  # Modify 40% of contracts

    for _, contract in modified_contracts.iterrows():
        contract_id = contract["contract_id"]
        agreed_price = float(contract["agreed_price"])

        # Handle missing deadlines by using the contract's start date instead
        deadline = contract["end_date"] if pd.notna(contract["end_date"]) else contract["start_date"]

        # Ensure deadline is a string
        if not isinstance(deadline, str) or deadline.strip() == "":
            continue  # Skip if no valid deadline is available

        # Get a random user (client or freelancer) to modify the contract
        modified_by = random.choice([contract["client_id"], contract["freelancer_id"]])

        num_modifications = random.randint(1, 3)  # Random history of 1 to 3 modifications

        for i in range(num_modifications):
            old_price = round(agreed_price * random.uniform(0.8, 1.2), 2)  # 80% to 120% of final price
            new_price = agreed_price if i == num_modifications - 1 else round(old_price * random.uniform(0.9, 1.1), 2)

            # Convert deadline to a proper date format
            try:
                old_deadline = (datetime.strptime(deadline, '%Y-%m-%d') - timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')
                new_deadline = deadline if i == num_modifications - 1 else (
                    datetime.strptime(old_deadline, '%Y-%m-%d') + timedelta(days=random.randint(5, 20))
                ).strftime('%Y-%m-%d')
            except ValueError:
                continue  # Skip this contract if date format is incorrect

            status = "approved"

            modification_queries.append(
                f"INSERT INTO contract_modifications (contract_id, modified_by, old_price, new_price, old_deadline, new_deadline, status) "
                f"VALUES ('{contract_id}', '{modified_by}', {old_price}, {new_price}, '{old_deadline}', '{new_deadline}', '{status}');"
            )

    # Create a few new `pending` or `rejected` modifications
    for _ in range(5):  # Generate 5 new modification requests
        contract = contracts_df.sample(1).iloc[0]
        contract_id = contract["contract_id"]
        modified_by = random.choice([contract["client_id"], contract["freelancer_id"]])
        agreed_price = float(contract["agreed_price"])

        old_price = round(agreed_price * random.uniform(0.8, 1.2), 2)
        new_price = round(old_price * random.uniform(0.9, 1.1), 2)

        old_deadline = (datetime.today() - timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')
        new_deadline = (datetime.today() + timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')

        status = random.choice(["pending", "rejected"])

        modification_queries.append(
            f"INSERT INTO contract_modifications (contract_id, modified_by, old_price, new_price, old_deadline, new_deadline, status) "
            f"VALUES ('{contract_id}', '{modified_by}', {old_price}, {new_price}, '{old_deadline}', '{new_deadline}', '{status}');"
        )

    # Save queries to a file
    with open("insert_contract_modifications.sql", "w") as f:
        f.write("\n".join(modification_queries))

    print(f"SQL file generated successfully: insert_contract_modifications.sql ({len(modification_queries)} modifications)")

# Example Usage:
generate_contract_modification_queries("contractmod/contracts.csv", "contractmod/users.csv")
