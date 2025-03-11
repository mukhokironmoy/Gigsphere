import random
import pandas as pd
from datetime import datetime, timedelta

def generate_submission_queries(contracts_csv, freelancers_csv):
    # Load contracts and freelancers data
    contracts_df = pd.read_csv(contracts_csv, dtype=str)
    freelancers_df = pd.read_csv(freelancers_csv, dtype=str)

    submission_queries = []

    # Filter only active contracts
    active_contracts = contracts_df[contracts_df["status"] == "active"]

    for _, contract in active_contracts.iterrows():
        contract_id = contract["contract_id"]
        freelancer_id = contract["freelancer_id"]

        # Ensure freelancer exists
        if freelancer_id in freelancers_df["freelancer_id"].values:
            # Generate a random submission description
            description = random.choice([
                "Initial draft submitted for review.",
                "Final version of the project submission.",
                "Updated files after feedback from client.",
                "Code repository and documentation uploaded.",
                "Design assets and project files attached."
            ])

            # Generate a random file name (simulating an uploaded submission)
            submitted_file = f"https://submissions.example.com/{freelancer_id}_{contract_id}.zip"

            # Generate random submission date within 15 days of today
            submitted_at = (datetime.today() - timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d %H:%M:%S')

            submission_queries.append(
                f"INSERT INTO submissions (submitted_by, contract_id, description, submitted_file, submitted_at, approved) "
                f"VALUES ('{freelancer_id}', '{contract_id}', '{description}', '{submitted_file}', '{submitted_at}', FALSE);"
            )

    # Save queries to a file
    with open("insert_submissions.sql", "w") as f:
        f.write("\n".join(submission_queries))

    print(f"SQL file generated successfully: insert_submissions.sql ({len(submission_queries)} submissions)")

# Example Usage:
generate_submission_queries("submissions/contracts.csv", "submissions/freelancers.csv")
