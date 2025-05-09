--VIEW FOR FREELANCER SKILLS

CREATE VIEW freelancer_skill_view AS
SELECT 
    f.freelancer_id,
    u.first_name,
    u.last_name,
    s.skill_name
FROM 
    freelancers f
JOIN 
    users u ON f.freelancer_id = u.user_id
JOIN 
    freelancer_skills fs ON f.freelancer_id = fs.freelancer_id
JOIN 
    skills s ON fs.skill_id = s.skill_id
ORDER BY 
    f.freelancer_id, s.skill_name;
	
----------------------------------------------------------------------------------------------------------------------------------------
