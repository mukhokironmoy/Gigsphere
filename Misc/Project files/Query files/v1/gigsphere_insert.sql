-- Insert users
INSERT INTO users (name, email, password_hash, user_type) VALUES
('Sample User1', 'user1@example.com', 'hashed_password1', 'freelancer'),
('Sample User2', 'user2@example.com', 'hashed_password2', 'client'),
('Sample User3', 'user3@example.com', 'hashed_password3', 'freelancer'),
('Sample User4', 'user4@example.com', 'hashed_password4', 'client'),
('Sample User5', 'user5@example.com', 'hashed_password5', 'freelancer'),
('Sample User6', 'user6@example.com', 'hashed_password6', 'client'),
('Sample User7', 'user7@example.com', 'hashed_password7', 'freelancer'),
('Sample User8', 'user8@example.com', 'hashed_password8', 'client'),
('Sample User9', 'user9@example.com', 'hashed_password9', 'freelancer'),
('Sample User10', 'user10@example.com', 'hashed_password10', 'client'),
('Sample User11', 'user11@example.com', 'hashed_password11', 'freelancer'),
('Sample User12', 'user12@example.com', 'hashed_password12', 'client'),
('Sample User13', 'user13@example.com', 'hashed_password13', 'freelancer'),
('Sample User14', 'user14@example.com', 'hashed_password14', 'client'),
('Sample User15', 'user15@example.com', 'hashed_password15', 'client');

select * from users;

-- Insert freelancers
INSERT INTO freelancers (freelancer_id, bio, experience, hourly_rate, portfolio) VALUES
(1, 'Experienced web developer', 3, 20.00, 'portfolio1.com'),
(3, 'Graphic designer with 5 years of experience', 5, 30.00, 'portfolio2.com'),
(5, 'Software engineer specializing in Python', 2, 25.00, 'portfolio3.com'),
(7, 'Digital marketer and SEO expert', 4, 40.00, 'portfolio4.com'),
(9, 'Data analyst with a focus on ML', 6, 50.00, 'portfolio5.com'),
(11, 'Beginner frontend developer', 1, 15.00, 'portfolio6.com'),
(13, 'Blockchain developer', 7, 60.00, 'portfolio7.com');

select * from freelancers

-- Insert users
INSERT INTO clients (client_id, company_name, business_type) VALUES
(2, 'Tech Solutions Ltd.', 'IT'),
(4, 'Creative Media Agency', 'Marketing'),
(6, 'Global Finance Corp', 'Finance'),
(8, 'Health First Inc.', 'Healthcare'),
(10, 'E-Shop International', 'E-commerce'),
(12, 'EduTech Academy', 'Education'),
(14, 'Real Estate Builders', 'Real Estate'),
(15, 'Consulting Experts Ltd.', 'Consulting');

select * from clients


--Inserting skills
INSERT INTO skills (skill_name) VALUES
('Skill 1'),
('Skill 2'),
('Skill 3'),
('Skill 4'),
('Skill 5'),
('Skill 6'),
('Skill 7');

select * from skills

--Inserting freelancer skills
INSERT INTO freelancer_skills (freelancer_id, skill_id) VALUES
(1, 1),
(3, 2),
(5, 3),
(7, 4),
(9, 5),
(11, 6),
(13, 7);

select * from freelancer_skills


--Inserting projects
INSERT INTO projects (client_id, title, description, budget, deadline, status) VALUES
(2, 'Project Title 1', 'Sample project description.', 5000.00, '2025-03-01', 'open'),
(4, 'Project Title 2', 'Sample project description.', 1000.00, '2025-02-15', 'open'),
(6, 'Project Title 3', 'Sample project description.', 3000.00, '2025-03-10', 'open'),
(8, 'Project Title 4', 'Sample project description.', 2500.00, '2025-04-01', 'open'),
(10, 'Project Title 5', 'Sample project description.', 4000.00, '2025-03-20', 'open'),
(12, 'Project Title 6', 'Sample project description.', 3500.00, '2025-02-28', 'open'),
(14, 'Project Title 7', 'Sample project description.', 8000.00, '2025-05-01', 'open'),
(15, 'Project Title 8', 'Sample project description.', 6000.00, '2025-06-01', 'open');

select * from projects


--Inserting proposals	
INSERT INTO proposals (project_id, freelancer_id, bid_amount, proposal_text, status) VALUES
(1, 1, 4500.00, 'Sample proposal text.', 'pending'),
(2, 3, 950.00, 'Sample proposal text.', 'accepted'),
(3, 5, 2800.00, 'Sample proposal text.', 'pending'),
(4, 7, 2300.00, 'Sample proposal text.', 'accepted'),
(5, 9, 3900.00, 'Sample proposal text.', 'pending'),
(6, 11, 3300.00, 'Sample proposal text.', 'rejected'),
(7, 13, 7800.00, 'Sample proposal text.', 'accepted'),
(8, 1, 5800.00, 'Sample proposal text.', 'pending');

select * from proposals


--Inserting contracts
INSERT INTO contracts (proposal_id, project_id, freelancer_id, start_date, end_date, agreed_price, status) VALUES
(2, 2, 3, '2025-02-01', '2025-02-15', 950.00, 'completed'),
(4, 4, 7, '2025-02-10', '2025-03-10', 2300.00, 'active'),
(7, 7, 13, '2025-03-01', '2025-05-01', 7800.00, 'active');

SELECT setval(
  'contracts_contract_id_seq', 
  COALESCE((SELECT MAX(contract_id) FROM contracts), 1), 
  FALSE
);


truncate table contracts cascade
select * from contracts

--Inserting payments
INSERT INTO payments (contract_id, amount, payment_method, status) VALUES
(1, 950.00, 'Credit Card', 'completed'),
(2, 2300.00, 'PayPal', 'pending'),
(3, 7800.00, 'Bank Transfer', 'pending');

SELECT setval(
  'payments_payment_id_seq', 
  COALESCE((SELECT MAX(payment_id) FROM payments), 1), 
  FALSE
);

truncate table payments cascade
select * from payments


--Inserting reviews
INSERT INTO reviews (reviewer_id, reviewee_id, project_id, rating, review_text) VALUES
(2, 3, 2, 5, 'Sample review text.'),
(4, 7, 4, 4, 'Sample review text.'),
(14, 13, 7, 5, 'Sample review text.');

SELECT setval(
  'reviews_review_id_seq', 
  COALESCE((SELECT MAX(review_id) FROM reviews), 1), 
  FALSE
);

select * from reviews

