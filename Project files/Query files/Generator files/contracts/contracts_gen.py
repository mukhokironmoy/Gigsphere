import pandas as pd
import random
from datetime import datetime, timedelta

def generate_contract_queries(proposals_csv, projects_csv, freelancers_csv, clients_csv):
    # Load data from CSVs
    proposals_df = pd.read_csv(proposals_csv, dtype=str)
    projects_df = pd.read_csv(projects_csv, dtype=str)
    freelancers_df = pd.read_csv(freelancers_csv, dtype=str)
    clients_df = pd.read_csv(clients_csv, dtype=str)

    contract_queries = []

    for _, proposal in proposals_df.iterrows():
        freelancer_id = proposal['freelancer_id']
        project_id = proposal['project_id']
        proposal_id = proposal['proposal_id']
        bid_amount = proposal['bid_amount']

        # Validate project and client
        project = projects_df[projects_df['project_id'] == project_id]
        if not project.empty:
            client_id = project.iloc[0]['client_id']
            deadline = project.iloc[0]['deadline']

            # Ensure client exists
            if client_id in clients_df['client_id'].values and freelancer_id in freelancers_df['freelancer_id'].values:
                # Generate random contract start date (within 30 days of today)
                start_date = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')

                # Set end date based on project deadline
                end_date = deadline if random.choice([True, False]) else None

                # Random contract status
                status = random.choice(["active", "completed", "cancelled"])

                contract_queries.append(
                    f"INSERT INTO contracts (client_id, freelancer_id, project_id, proposal_id, agreed_price, start_date, end_date, status) "
                    f"VALUES ('{client_id}', '{freelancer_id}', '{project_id}', '{proposal_id}', {bid_amount}, '{start_date}', "
                    f"{f'NULL' if end_date is None else f'\'{end_date}\''}, '{status}');"
                )

    # Save queries to a file
    with open("insert_contracts.sql", "w") as f:
        f.write("\n".join(contract_queries))

    print(f"SQL file generated successfully: insert_contracts.sql ({len(contract_queries)} contracts)")

# Example Usage:
generate_contract_queries("contracts/proposals.csv", "contracts/projects.csv", "contracts/freelancers.csv", "contracts/clients.csv")
