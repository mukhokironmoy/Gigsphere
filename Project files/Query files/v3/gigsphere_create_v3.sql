CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- Ensure UUID functions are available

CREATE TABLE users (
    user_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type VARCHAR(50) CHECK(user_type IN ('client', 'freelancer')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_hash VARCHAR(50) NOT NULL
);

CREATE TABLE clients (
    client_id CHAR(10) PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    company_name VARCHAR(50),
    business_type VARCHAR(50)
);

CREATE TABLE projects (
    project_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    client_id CHAR(10) REFERENCES clients(client_id) ON DELETE CASCADE,
    title VARCHAR(200),
    description TEXT,
    budget DECIMAL(10,2) CHECK(budget >= 0),
    deadline DATE NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) CHECK(status IN ('open', 'in progress', 'completed', 'cancelled'))
);

CREATE TABLE freelancers (
    freelancer_id CHAR(10) PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    bio TEXT,
    portfolio TEXT,
    experience INT CHECK(experience >= 0),
    hourly_rate DECIMAL(10,2) CHECK(hourly_rate >= 0)
);

CREATE TABLE skills (
    skill_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    skill_name VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE freelancer_skills (
    skill_id CHAR(10) REFERENCES skills(skill_id) ON DELETE CASCADE,
    freelancer_id CHAR(10) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    PRIMARY KEY (skill_id, freelancer_id)
);

CREATE TABLE proposals (
    proposal_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    freelancer_id CHAR(10) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    project_id CHAR(10) REFERENCES projects(project_id) ON DELETE CASCADE,
    proposal_text TEXT NOT NULL,
    bid_amount DECIMAL(10,2) CHECK(bid_amount >= 0),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    review_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    reviewer_id CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    reviewee_id CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    review_text TEXT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE endorsements (
    endorsement_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    client_id CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    freelancer_id CHAR(10) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    endorsement_text TEXT
);

CREATE TABLE contracts (
    contract_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    client_id CHAR(10) REFERENCES clients(client_id) ON DELETE CASCADE,
    freelancer_id CHAR(10) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    project_id CHAR(10) REFERENCES projects(project_id) ON DELETE CASCADE,
    proposal_id CHAR(10) REFERENCES proposals(proposal_id) ON DELETE CASCADE,
    agreed_price DECIMAL(10,2) CHECK(agreed_price >= 0),
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) CHECK(status IN ('active', 'completed', 'cancelled'))
);

CREATE TABLE contract_modifications (
    modification_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    contract_id CHAR(10) REFERENCES contracts(contract_id) ON DELETE CASCADE,
    modified_by CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    old_deadline DATE,
    new_deadline DATE,
    status VARCHAR(50) CHECK(status IN ('pending', 'approved', 'rejected'))
);

CREATE TABLE payments (
    payment_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    contract_id CHAR(10) REFERENCES contracts(contract_id) ON DELETE CASCADE,
    amount DECIMAL(10,2) CHECK(amount >= 0),
    payment_method VARCHAR(100) NOT NULL,
    status VARCHAR(50) CHECK(status IN ('completed', 'failed'))
);

CREATE TABLE invoices (
    invoice_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    contract_id CHAR(10) REFERENCES contracts(contract_id) ON DELETE CASCADE,
    net_amount DECIMAL(10,2) CHECK(net_amount >= 0),
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    status VARCHAR(50) CHECK(status IN ('pending', 'paid', 'overdue')),
    paid_at TIMESTAMP
);

CREATE TABLE submissions (
    submission_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    submitted_by CHAR(10) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
    contract_id CHAR(10) REFERENCES contracts(contract_id) ON DELETE CASCADE,
    description TEXT,
    submitted_file VARCHAR(500),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved BOOLEAN DEFAULT FALSE
);

CREATE TABLE withdrawals (
    withdrawal_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    requested_by CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    approved_by CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    contract_id CHAR(10) REFERENCES contracts(contract_id) ON DELETE CASCADE,
    reason TEXT,
    status VARCHAR(50) CHECK(status IN ('pending', 'approved', 'rejected')),
    withdrawn_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
    ticket_id CHAR(10) PRIMARY KEY DEFAULT substring(gen_random_uuid()::TEXT FROM 1 FOR 10),
    raised_by CHAR(10) REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subject VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) CHECK(status IN ('open', 'in progress', 'resolved', 'closed')),
    resolved_at TIMESTAMP
);


-- View names of all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

DROP TABLE IF EXISTS 
    support_tickets,
    withdrawals,
    submissions,
    invoices,
    payments,
    contract_modifications,
    contracts,
    endorsements,
    reviews,
    proposals,
    freelancer_skills,
    skills,
    freelancers,
    projects,
    clients,
    users 
CASCADE;

select * from contracts;