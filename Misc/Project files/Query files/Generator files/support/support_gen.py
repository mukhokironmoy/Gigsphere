import random
import pandas as pd
from datetime import datetime, timedelta

def generate_support_ticket_queries(users_csv):
    # Load users data
    users_df = pd.read_csv(users_csv, dtype=str)

    ticket_queries = []

    # Only a small percentage of users will raise support tickets
    num_tickets = max(5, len(users_df) // 10)  # At most 10% of users raise tickets

    # Sample random users to raise support tickets
    selected_users = users_df.sample(n=num_tickets)

    subjects = [
        "Payment not processed",
        "Issue with project submission",
        "Unable to withdraw funds",
        "Account verification pending",
        "Bug in contract approval system",
        "Freelancer not responding",
        "Client not providing feedback",
        "Login issues",
        "Profile update not saving",
        "Other general inquiry"
    ]

    for _, user in selected_users.iterrows():
        raised_by = user["user_id"]
        subject = random.choice(subjects)
        description = f"User {raised_by} reported an issue: {subject.lower()}."

        # Randomly assign status
        status = random.choice(["open", "in progress", "resolved", "closed"])

        # If ticket is resolved or closed, add a resolved_at date
        resolved_at = (
            f"'{(datetime.today() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')}'"
            if status in ["resolved", "closed"]
            else "NULL"
        )

        ticket_queries.append(
            f"INSERT INTO support_tickets (raised_by, subject, description, status, resolved_at) "
            f"VALUES ('{raised_by}', '{subject}', '{description}', '{status}', {resolved_at});"
        )

    # Save queries to a file
    with open("insert_support_tickets.sql", "w") as f:
        f.write("\n".join(ticket_queries))

    print(f"SQL file generated successfully: insert_support_tickets.sql ({len(ticket_queries)} tickets)")

# Example Usage:
generate_support_ticket_queries("support/users.csv")
