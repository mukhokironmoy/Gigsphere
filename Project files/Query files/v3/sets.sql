-- Find all users who are either freelancers or clients
SELECT user_id, username, 'Freelancer' AS role FROM users
WHERE user_id IN (SELECT freelancer_id FROM freelancers)
UNION
SELECT user_id, username, 'Client' AS role FROM users
WHERE user_id IN (SELECT client_id FROM clients);

--Find users who are both freelancers and have received endorsements
SELECT freelancer_id FROM freelancers
INTERSECT
SELECT freelancer_id FROM endorsements;

--Find freelancers who have skills but have never submitted a proposal
SELECT freelancer_id FROM freelancer_skills
EXCEPT
SELECT freelancer_id FROM proposals;

--Find projects that have received proposals but have not been converted into contracts
SELECT project_id FROM proposals
EXCEPT
SELECT project_id FROM contracts;
