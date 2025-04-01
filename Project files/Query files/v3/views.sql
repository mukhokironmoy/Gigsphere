-- View of projects with proposal count
CREATE VIEW project_proposal_count AS
SELECT p.project_id, p.title, COUNT(pr.proposal_id) AS proposal_count
FROM projects p
LEFT JOIN proposals pr ON p.project_id = pr.project_id
GROUP BY p.project_id;

select * from project_proposal_count

--View of freelancer with their skills
CREATE VIEW freelancer_skill_summary AS
SELECT f.freelancer_id, u.username, STRING_AGG(s.skill_name, ', ') AS skills
FROM freelancers f
JOIN users u ON f.freelancer_id = u.user_id
JOIN freelancer_skills fs ON f.freelancer_id = fs.freelancer_id
JOIN skills s ON fs.skill_id = s.skill_id
GROUP BY f.freelancer_id, u.username;

select * from freelancer_skill_summary

-- view for projects that have not received any submissions within the deadline
CREATE VIEW projects_without_submissions AS
SELECT 
    p.project_id, 
    p.title AS project_title, 
    p.deadline
FROM projects p
LEFT JOIN contracts c ON p.project_id = c.project_id
LEFT JOIN submissions s ON c.contract_id = s.contract_id
WHERE s.submission_id IS NULL 
AND p.deadline < CURRENT_DATE;

SELECT * FROM projects_without_submissions;

-- view for withdrawn contracts and refundable amounts
CREATE VIEW withdrawn_contracts_refund AS
SELECT 
    c.contract_id, 
    COALESCE(SUM(p.amount), 0) AS refund_amount
FROM contracts c
LEFT JOIN payments p ON c.contract_id = p.contract_id
WHERE c.status = 'withdrawn'
GROUP BY c.contract_id;

SELECT * FROM withdrawn_contracts_refund;



