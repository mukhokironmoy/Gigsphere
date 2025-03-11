CREATE TABLE users(
user_id SERIAL PRIMARY KEY,
username VARCHAR(20) UNIQUE NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
user_type VARCHAR(50) CHECK(user_type IN ('client', 'freelancer')) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
password_hash VARCHAR(50) NOT NULL
);

CREATE TABLE clients(
client_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
company_name VARCHAR(50),
business_type VARCHAR(50)
);

CREATE TABLE projects(
project_id SERIAL PRIMARY KEY,
client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
title VARCHAR(200) NOT NULL,
description TEXT,
budget DECIMAL(10,2) CHECK(budget>=0),
deadline DATE NOT NULL,
posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
status VARCHAR(50) CHECK(status IN ('open', 'in progress', 'completed', 'cancelled'))
);

CREATE TABLE freelancers(
freelancer_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
bio TEXT,
portfolio TEXT,
experience INT CHECK(experience>=0),
hourly_rate DECIMAL(10,2) CHECK(hourly_rate>=0)
);

CREATE TABLE skills(
skill_id SERIAL PRIMARY KEY,
skill_name VARCHAR(300) UNIQUE NOT NULL
);

CREATE TABLE freelancer_skills(
skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE,
freelancer_id INT REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
PRIMARY KEY(skill_id, freelancer_id)
);

CREATE TABLE proposals(
proposal_id SERIAL PRIMARY KEY,
freelancer_id INT REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
proposal_text TEXT,
bid_amount DECIMAL(10,2) CHECK(bid_amount>=0),
submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
status VARCHAR(50) CHECK (status IN ('pending', 'accepted', 'rejected'))
);

CREATE TABLE reviews(
review_id SERIAL PRIMARY KEY,
reviewer_id INT REFERENCES users(user_id) ON DELETE CASCADE,
reviewee_id INT REFERENCES users(user_id) ON DELETE CASCADE,
project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
review_text TEXT,
rating INT CHECK(rating BETWEEN 1 AND 5) NOT NULL,
review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--View names of all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';