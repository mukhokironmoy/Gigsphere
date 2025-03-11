--Creating the Users table
CREATE TABLE users(
user_id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password_hash VARCHAR(255) NOT NULL,
user_type VARCHAR(20) CHECK (user_type IN ('client', 'freelancer')) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Creating the Freelancers table
CREATE TABLE freelancers(
freelancer_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
bio TEXT,
experience INT CHECK (experience >=0),
hourly_rate DECIMAL(10,2) CHECK (hourly_rate>=0),
portfolio VARCHAR(500)
);

--Creating the Skills table
CREATE TABLE skills(
skill_id SERIAL PRIMARY KEY,
skill_name VARCHAR(255) UNIQUE NOT NULL
);


--Creating the Freelancer skills table
CREATE TABLE freelancer_skills(
freelancer_id INT REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE,
PRIMARY KEY (freelancer_id, skill_id)
);

--Creating the Clients table
CREATE TABLE clients(
client_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
company_name VARCHAR(255),
business_type VARCHAR(255)
);

--Creating the Projects table
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    budget DECIMAL(10,2) CHECK (budget >= 0),
    deadline DATE NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) CHECK (status IN ('open', 'in progress', 'completed', 'cancelled'))
);

--Creating the Reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    reviewer_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    reviewee_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(project_id) ON DELETE SET NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--Creating the Proporsals table
CREATE TABLE proposals (
    proposal_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    freelancer_id INT REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    bid_amount DECIMAL(10,2) CHECK (bid_amount >= 0),
    proposal_text TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) CHECK (status IN ('pending', 'accepted', 'rejected'))
);

--Creating the Contracts table
CREATE TABLE contracts (
    contract_id SERIAL PRIMARY KEY,
    proposal_id INT REFERENCES proposals(proposal_id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
    freelancer_id INT REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    agreed_price DECIMAL(10,2) CHECK (agreed_price >= 0),
    status VARCHAR(50) CHECK (status IN ('active', 'completed', 'cancelled'))
);


--Creating the Payments table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    contract_id INT REFERENCES contracts(contract_id) ON DELETE CASCADE,
    amount DECIMAL(10,2) CHECK (amount >= 0),
    payment_method VARCHAR(100) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('pending', 'completed', 'failed'))
);

--View names of all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';




