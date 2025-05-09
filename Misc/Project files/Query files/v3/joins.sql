--INNER JOIN
--Get all freelancers and the skills they have:
SELECT f.freelancer_id, u.username, s.skill_name
FROM freelancers f
INNER JOIN users u ON f.freelancer_id = u.user_id
INNER JOIN freelancer_skills fs ON f.freelancer_id = fs.freelancer_id
INNER JOIN skills s ON fs.skill_id = s.skill_id;

--LEFT JOIN
--Get all projects and the proposals received (if any):
SELECT p.project_id, p.title, pr.proposal_id, pr.bid_amount
FROM projects p
LEFT JOIN proposals pr ON p.project_id = pr.project_id;

--RIGHT JOIN
--Get all freelancers, and the proposals they made (if any):
SELECT f.freelancer_id, u.username, pr.proposal_id, pr.bid_amount
FROM proposals pr
RIGHT JOIN freelancers f ON pr.freelancer_id = f.freelancer_id
RIGHT JOIN users u ON f.freelancer_id = u.user_id;

--FULL OUTER JOIN
--List all users and the reviews they’ve written or received, even if there’s no match on either side:
SELECT u.user_id, u.username, r.review_text, r.rating
FROM users u
FULL OUTER JOIN reviews r
ON u.user_id = r.reviewer_id OR u.user_id = r.reviewee_id;
