import random
import pandas as pd

def generate_project_queries(csv_file):
    # Load the clients data
    df = pd.read_csv(csv_file, dtype=str)  # Ensure client_id is read as a string
    
    project_queries = []
    
    for _, row in df.iterrows():
        client_id = row['client_id']
        
        num_projects = random.randint(1, 5)  # Each client gets between 1 to 5 projects
        
        for _ in range(num_projects):
            title = random.choice([
                "E-commerce Website Development", "Marketing Campaign Strategy",
                "Mobile App UI/UX Design", "SEO Optimization Project",
                "Data Analysis and Reporting", "AI Chatbot Development",
                "Logo and Branding Package", "Social Media Content Creation",
                "Financial Consulting Services", "Custom CRM Development"
            ])
            
            description = f"This project focuses on {title.lower()} with a detailed plan."
            budget = round(random.uniform(500, 10000), 2)  # Random budget between $500 and $10,000
            deadline = f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"  # Random date in 2025
            status = random.choice(["open", "in progress", "completed", "cancelled"])
            
            project_queries.append(f"INSERT INTO projects (client_id, title, description, budget, deadline, status) "
                                   f"VALUES ('{client_id}', '{title}', '{description}', {budget}, '{deadline}', '{status}');")
    
    # Save the queries to a file
    with open("insert_projects.sql", "w") as f:
        f.write("\n".join(project_queries))
    
    print(f"SQL file generated successfully: insert_projects.sql ({len(project_queries)} projects)")

# Example Usage:
generate_project_queries("D:/Learning/DBMS Project/Project files/Query files/Generator files/projects/clients.csv")
