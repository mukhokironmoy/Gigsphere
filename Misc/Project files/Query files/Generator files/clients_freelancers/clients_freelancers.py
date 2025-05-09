import random
import pandas as pd

def generate_insert_queries(csv_file):
    # Load the users data
    df = pd.read_csv(csv_file, dtype=str)  # Ensure user_id is read as a string
    
    clients_queries = []
    freelancers_queries = []
    
    for _, row in df.iterrows():
        user_id = row['user_id']
        user_type = row['user_type']
        
        if user_type == "client":
            company_name = f"Company_{random.randint(1, 100)}"
            business_type = random.choice(["Tech", "Finance", "Marketing", "E-commerce", "Healthcare"])
            clients_queries.append(f"INSERT INTO clients (client_id, company_name, business_type) "
                                   f"VALUES ('{user_id}', '{company_name}', '{business_type}');")
        
        elif user_type == "freelancer":
            bio = f"Experienced {random.choice(['developer', 'designer', 'writer', 'marketer'])}"
            portfolio = f"https://portfolio.com/{user_id[:5]}"
            experience = random.randint(0, 15)
            hourly_rate = round(random.uniform(10, 150), 2)
            freelancers_queries.append(f"INSERT INTO freelancers (freelancer_id, bio, portfolio, experience, hourly_rate) "
                                       f"VALUES ('{user_id}', '{bio}', '{portfolio}', {experience}, {hourly_rate});")
    
    # Save the queries to files
    with open("insert_clients.sql", "w") as f:
        f.write("\n".join(clients_queries))
    
    with open("insert_freelancers.sql", "w") as f:
        f.write("\n".join(freelancers_queries))
    
    print("SQL files generated successfully: insert_clients.sql, insert_freelancers.sql")

# Example Usage:
generate_insert_queries("users.csv")
