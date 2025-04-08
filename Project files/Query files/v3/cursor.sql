--Fetch Pending Invoices and Mark as Overdue If Past Due Date
CREATE OR REPLACE FUNCTION mark_overdue_invoices()
RETURNS VOID AS $$
DECLARE
    invoice_cursor CURSOR FOR 
    SELECT invoice_id, due_date FROM invoices WHERE status = 'pending' AND due_date < NOW();
    invoice_record RECORD;
BEGIN
    FOR invoice_record IN invoice_cursor LOOP
        UPDATE invoices SET status = 'overdue' WHERE invoice_id = invoice_record.invoice_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT invoice_id, due_date FROM invoices WHERE status = 'pending' AND due_date < NOW();
SELECT mark_overdue_invoices();
SELECT invoice_id, due_date FROM invoices WHERE status = 'pending' AND due_date < NOW();
rollback;


--Automatically Increase Budget for Overdue Projects
CREATE OR REPLACE FUNCTION increase_budget_for_overdue_projects()
RETURNS VOID AS $$
DECLARE
    project_cursor CURSOR FOR 
    SELECT project_id, budget FROM projects WHERE deadline < NOW();
    project_record RECORD;
BEGIN
    FOR project_record IN project_cursor LOOP
        UPDATE projects 
        SET budget = budget * 1.1
        WHERE project_id = project_record.project_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT project_id, budget FROM projects WHERE deadline < NOW();
SELECT increase_budget_for_overdue_projects();
SELECT project_id, budget FROM projects WHERE deadline < NOW();


--Assign Default Status to Projects Missing a Status
CREATE OR REPLACE FUNCTION update_missing_project_status()
RETURNS VOID AS $$
DECLARE
    project_cursor CURSOR FOR 
    SELECT project_id FROM projects WHERE status IS NULL;
    project_record RECORD;
BEGIN
    FOR project_record IN project_cursor LOOP
        UPDATE projects 
        SET status = 'open' 
        WHERE project_id = project_record.project_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT update_missing_project_status();
SELECT project_id FROM projects WHERE status IS NULL;


--Mark Completed Projects as Closed
CREATE OR REPLACE FUNCTION close_completed_projects()
RETURNS VOID AS $$
DECLARE
    project_cursor CURSOR FOR 
    SELECT project_id FROM projects 
    WHERE end_date < NOW() AND status = 'open';
    project_record RECORD;
BEGIN
    FOR project_record IN project_cursor LOOP
        UPDATE projects 
        SET status = 'closed' 
        WHERE project_id = project_record.project_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


SELECT project_id FROM projects WHERE end_date < NOW() AND status = 'open';
SELECT close_completed_projects();
SELECT project_id FROM projects WHERE end_date < NOW() AND status = 'open';






