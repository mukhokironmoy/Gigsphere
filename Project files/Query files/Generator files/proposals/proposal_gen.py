import random
import pandas as pd

def generate_proposal_queries(freelancers_csv, projects_csv):
    # Load the freelancers and projects data
    freelancers_df = pd.read_csv(freelancers_csv, dtype=str)
    projects_df = pd.read_csv(projects_csv, dtype=str)

    proposal_queries = []

    for _, freelancer in freelancers_df.iterrows():
        freelancer_id = freelancer['freelancer_id']

        # Each freelancer bids on 1 to 5 random projects
        num_proposals = random.randint(1, 5)
        projects_sample = projects_df.sample(n=min(num_proposals, len(projects_df)))

        for _, project in projects_sample.iterrows():
            project_id = project['project_id']

            # Generate a random bid amount within a range
            min_budget = float(project['budget']) * 0.8  # 80% of project budget
            max_budget = float(project['budget']) * 1.2  # 120% of project budget
            bid_amount = round(random.uniform(min_budget, max_budget), 2)

            # Generate proposal text
            proposal_text = f"I am highly experienced in {project['title'].split()[0].lower()} and can deliver great results."

            proposal_queries.append(
                f"INSERT INTO proposals (freelancer_id, project_id, proposal_text, bid_amount) "
                f"VALUES ('{freelancer_id}', '{project_id}', '{proposal_text}', {bid_amount});"
            )

    # Save the queries to a file
    with open("insert_proposals.sql", "w") as f:
        f.write("\n".join(proposal_queries))

    print(f"SQL file generated successfully: insert_proposals.sql ({len(proposal_queries)} proposals)")

# Example Usage:
generate_proposal_queries("proposals/freelancers.csv", "proposals/projects.csv")
