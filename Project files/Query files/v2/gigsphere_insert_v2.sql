INSERT INTO users (username, email, user_type, password_hash) VALUES
('AmitSharma', 'amit.sharma@example.com', 'client', 'pass123'),
('PriyaVerma', 'priya.verma@example.com', 'freelancer', 'secure456'),
('RahulNair', 'rahul.nair@example.com', 'client', 'pwd789'),
('AnanyaRao', 'ananya.rao@example.com', 'freelancer', 'test111'),
('VikasPatel', 'vikas.patel@example.com', 'client', 'hashed234'),
('SnehaIyer', 'sneha.iyer@example.com', 'freelancer', 'mypass345'),
('KaranJoshi', 'karan.joshi@example.com', 'client', 'abc987'),
('RohitMishra', 'rohit.mishra@example.com', 'freelancer', 'xyz999'),
('DeepikaSingh', 'deepika.singh@example.com', 'client', 'safepass222'),
('ManojPillai', 'manoj.pillai@example.com', 'freelancer', 'final999');

INSERT INTO clients (client_id, company_name, business_type) VALUES
(1, 'Sharma Tech Solutions', 'IT Services'),
(3, 'Nair Enterprises', 'Marketing'),
(5, NULL, 'Consulting'),
(7, 'Joshi Pvt Ltd', NULL),
(9, 'Singh Innovations', 'Product Development');

INSERT INTO projects (client_id, title, description, budget, deadline, status) VALUES
(1, 'E-commerce Website Development', 'Develop a Shopify store for an online business.', 5000.00, '2025-04-01', 'open'),
(3, 'Digital Marketing Strategy', 'SEO and social media plan for a startup.', 1500.00, '2025-03-15', 'in progress'),
(5, 'Business Analytics Dashboard', 'Build a Power BI dashboard for business analytics.', 3000.00, '2025-05-01', 'completed'),
(7, 'Company Branding & Logo Design', NULL, 1200.00, '2025-02-28', 'open'),
(9, 'Mobile App UI/UX Design', 'Create wireframes for a new fintech mobile app.', NULL, '2025-04-10', 'open');

INSERT INTO freelancers (freelancer_id, bio, portfolio, experience, hourly_rate) VALUES
(2, 'Web Developer with 5 years experience', 'https://priya-portfolio.com', 5, 25.00),
(4, 'Graphic Designer, loves UI/UX', NULL, 3, 20.00),
(6, 'Data Analyst with machine learning skills', 'https://sneha-portfolio.com', 4, NULL),
(8, 'Python and Django Expert', 'https://rohit-portfolio.com', 6, 35.00),
(10, NULL, NULL, 2, 15.00);

INSERT INTO skills (skill_name) VALUES
('Python'), ('ReactJS'), ('Data Analysis'), ('Graphic Design'), ('SEO'),
('Machine Learning'), ('WordPress Development'), ('Copywriting'), ('Cloud Computing'), ('Android Development');

INSERT INTO freelancer_skills (freelancer_id, skill_id) VALUES
(2, 1), (2, 2),
(4, 4),
(6, 3), (6, 6),
(8, 1), (8, 7), (8, 9),
(10, 8);

INSERT INTO proposals (freelancer_id, project_id, proposal_text, bid_amount) VALUES
(2, 1, 'I have 5 years of experience in web development.', 4800.00),
(4, 4, 'I can design a modern and professional brand identity.', 1100.00),
(6, 3, 'Experienced in data visualization and business analytics.', 2900.00),
(8, 1, 'Expert in Shopify development, delivering high-quality work.', 5000.00),
(10, 5, 'I can write compelling copy for your UI/UX design.', 500.00);

INSERT INTO reviews (reviewer_id, reviewee_id, review_text, rating) VALUES
(1, 2, 'Excellent work, delivered ahead of schedule!', 5),
(3, 6, 'Very professional and insightful data analytics.', 4),
(5, 4, 'Good design, but took longer than expected.', 3),
(7, 8, NULL, 4),
(9, 10, 'Great writing, highly recommended!', 5);

INSERT INTO endorsements (client_id, freelancer_id, endorsement_text) VALUES
(1, 2, 'Great web development skills, very professional.'),
(3, 6, 'Highly skilled in data analysis, insightful work.'),
(5, 4, 'Excellent creativity and branding sense.'),
(7, 8, 'Highly reliable freelancer, great technical expertise.'),
(9, 10, NULL);

INSERT INTO contracts (client_id, freelancer_id, project_id, proposal_id, agreed_price, start_date, end_date, status) VALUES
(1, 2, 1, 1, 4800.00, '2025-03-01', NULL, 'active'),
(3, 6, 3, 3, 2900.00, '2025-02-15', '2025-04-01', 'completed'),
(5, 4, 4, 2, 1100.00, '2025-02-20', NULL, 'active'),
(7, 8, 1, 4, 5000.00, '2025-03-05', '2025-04-15', 'active'),
(9, 10, 5, 5, 500.00, '2025-02-10', '2025-02-25', 'completed');

select * from contracts
truncate table contracts cascade;

SELECT setval(
  'contracts_contract_id_seq', 
  COALESCE((SELECT MAX(contract_id) FROM contracts), 1), 
  FALSE
);

INSERT INTO contract_modifications (contract_id, modified_by, modified_at, old_price, new_price, old_deadline, new_deadline, status) VALUES
(1, 1, '2025-03-05', 4800.00, 5000.00, NULL, '2025-04-10', 'approved'),
(3, 6, '2025-02-20', 2900.00, 2900.00, '2025-04-01', '2025-05-01', 'approved');

select * from contract_modifications;
truncate table contract_modifications cascade;
SELECT setval(
  'contract_modifications_modification_id_seq', 
  COALESCE((SELECT MAX(modification_id) FROM contract_modifications), 1), 
  FALSE
);

INSERT INTO payments (contract_id, amount, payment_method, status) VALUES
(1, 2000.00, 'Credit Card', 'completed'),
(1, 2800.00, 'Bank Transfer', 'completed'),
(3, 2900.00, 'UPI', 'completed');

INSERT INTO invoices (contract_id, net_amount, due_date, status) VALUES
(1, 5000.00, '2025-04-15', 'pending'),
(3, 2900.00, '2025-05-01', 'paid');

INSERT INTO submissions (submitted_by, contract_id, description, approved) VALUES
(2, 1, 'Final Shopify website.', TRUE);

INSERT INTO withdrawals (requested_by, contract_id, reason, status) VALUES
(2, 1, 'Freelancer unable to meet deadline.', 'approved');

INSERT INTO support_tickets (raised_by, subject, description, status) VALUES
(1, 'Issue with payment processing', 'My credit card payment failed twice.', 'open');

-- 1. Select all data from Users
SELECT * FROM users;

-- 2. Select all data from Clients
SELECT * FROM clients;

-- 3. Select all data from Projects
SELECT * FROM projects;

-- 4. Select all data from Freelancers
SELECT * FROM freelancers;

-- 5. Select all data from Skills
SELECT * FROM skills;

-- 6. Select all data from Freelancer Skills (Many-to-Many Mapping)
SELECT * FROM freelancer_skills;

-- 7. Select all data from Proposals
SELECT * FROM proposals;

-- 8. Select all data from Reviews
SELECT * FROM reviews;

-- 9. Select all data from Endorsements
SELECT * FROM endorsements;

-- 10. Select all data from Contracts
SELECT * FROM contracts;

-- 11. Select all data from Contract Modifications
SELECT * FROM contract_modifications;

-- 12. Select all data from Payments
SELECT * FROM payments;

-- 13. Select all data from Invoices
SELECT * FROM invoices;

-- 14. Select all data from Work Submissions
SELECT * FROM submissions;

-- 15. Select all data from Withdrawals
SELECT * FROM withdrawals;

-- 16. Select all data from Support Tickets
SELECT * FROM support_tickets;







