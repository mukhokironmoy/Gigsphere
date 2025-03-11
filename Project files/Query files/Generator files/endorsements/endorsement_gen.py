import pandas as pd

def generate_endorsement_queries(reviews_csv, users_csv, freelancers_csv):
    # Load reviews, users, and freelancers data
    reviews_df = pd.read_csv(reviews_csv, dtype=str)
    users_df = pd.read_csv(users_csv, dtype=str)
    freelancers_df = pd.read_csv(freelancers_csv, dtype=str)

    endorsement_queries = []

    # Filter reviews with a rating of 5
    five_star_reviews = reviews_df[reviews_df['rating'] == '5']

    for _, review in five_star_reviews.iterrows():
        client_id = review['reviewer_id']
        freelancer_id = review['reviewee_id']

        # Ensure client is a valid user and freelancer exists
        if client_id in users_df['user_id'].values and freelancer_id in freelancers_df['freelancer_id'].values:
            client = users_df[(users_df['user_id'] == client_id) & (users_df['user_type'] == 'client')]
            freelancer = freelancers_df[freelancers_df['freelancer_id'] == freelancer_id]

            if not client.empty and not freelancer.empty:
                endorsement_text = "Outstanding professionalism and expertise. Highly endorsed!"
                
                endorsement_queries.append(
                    f"INSERT INTO endorsements (client_id, freelancer_id, endorsement_text) "
                    f"VALUES ('{client_id}', '{freelancer_id}', '{endorsement_text}');"
                )

    # Save queries to a file
    with open("insert_endorsements.sql", "w") as f:
        f.write("\n".join(endorsement_queries))

    print(f"SQL file generated successfully: insert_endorsements.sql ({len(endorsement_queries)} endorsements)")

# Example Usage:
generate_endorsement_queries("endorsements/reviews.csv", "endorsements/users.csv", "endorsements/freelancers.csv")
