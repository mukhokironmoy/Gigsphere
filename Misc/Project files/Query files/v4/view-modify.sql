select * from users
select * from clients
select * from freelancers
select * from projects
select * from skills
select * from freelancer_skills
select * from freelancer_skill_view
select * from proposals
select * from reviews
select * from endorsements
select * from contracts
select * from invoices

ALTER TABLE freelancers ALTER COLUMN freelancer_id TYPE VARCHAR(25);
ALTER TABLE clients ALTER COLUMN client_id TYPE VARCHAR(25);
ALTER TABLE projects ALTER COLUMN client_id TYPE VARCHAR(25);
ALTER TABLE freelancer_skills ALTER COLUMN freelancer_id TYPE VARCHAR(25);
ALTER TABLE proposals ADD COLUMN status VARCHAR(50) CHECK(status IN ('accepted', 'rejected', 'approval pending'))
ALTER TABLE reviews ADD COLUMN project_id CHAR(10) REFERENCES projects(project_id) ON DELETE CASCADE
ALTER TABLE contracts ALTER COLUMN start_date SET NOT NULL;
ALTER TABLE contracts ALTER COLUMN start_date SET DEFAULT CURRENT_DATE;




