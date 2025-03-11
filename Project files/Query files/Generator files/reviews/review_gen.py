import random
import pandas as pd

def generate_review_queries(users_csv, projects_csv, proposals_csv):
    # Load users, projects, and proposals data
    users_df = pd.read_csv(users_csv, dtype=str)
    projects_df = pd.read_csv(projects_csv, dtype=str)
    proposals_df = pd.read_csv(proposals_csv, dtype=str)

    review_queries = []

    # Filter only completed projects
    completed_projects = projects_df[projects_df['status'] == 'completed']

    for _, project in completed_projects.iterrows():
        project_id = project['project_id']
        client_id = project['client_id']

        # Get freelancers who worked on this project
        freelancers = proposals_df[proposals_df['project_id'] == project_id]['freelancer_id'].unique()

        for freelancer_id in freelancers:
            # Ensure both users exist in users.csv
            if client_id in users_df['user_id'].values and freelancer_id in users_df['user_id'].values:
                reviewer = users_df[(users_df['user_id'] == client_id) & (users_df['user_type'] == 'client')]
                reviewee = users_df[(users_df['user_id'] == freelancer_id) & (users_df['user_type'] == 'freelancer')]

                if not reviewer.empty and not reviewee.empty:
                    # Generate rating (1 to 5)
                    rating = random.randint(1, 5)

                    # Generate review text based on rating
                    if rating == 5:
                        review_text = "Exceptional work! Highly recommended."
                    elif rating == 4:
                        review_text = "Great job, met expectations well."
                    elif rating == 3:
                        review_text = "Decent work, but could be improved."
                    elif rating == 2:
                        review_text = "Not fully satisfied, several issues."
                    else:
                        review_text = "Very disappointing, would not recommend."

                    review_queries.append(
                        f"INSERT INTO reviews (reviewer_id, reviewee_id, review_text, rating) "
                        f"VALUES ('{client_id}', '{freelancer_id}', '{review_text}', {rating});"
                    )

    # Save the queries to a file
    with open("insert_reviews.sql", "w") as f:
        f.write("\n".join(review_queries))

    print(f"SQL file generated successfully: insert_reviews.sql ({len(review_queries)} reviews)")

# Example Usage:
generate_review_queries("reviews/users.csv", "reviews/projects.csv", "reviews/proposals.csv")
