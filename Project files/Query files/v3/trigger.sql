-- Define the trigger function
CREATE OR REPLACE FUNCTION update_contract_status()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.approved = FALSE AND NEW.approved = TRUE THEN
        UPDATE contracts
        SET status = 'completed'
        WHERE contract_id = NEW.contract_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger that calls the function
CREATE TRIGGER trigger_update_contract
AFTER UPDATE ON submissions
FOR EACH ROW
WHEN (OLD.approved = FALSE AND NEW.approved = TRUE)
EXECUTE FUNCTION update_contract_status();

-- Query to view submissions that are not approved
SELECT s.submission_id, s.contract_id, s.approved, c.status AS contract_status
FROM submissions s
JOIN contracts c ON s.contract_id = c.contract_id
WHERE s.approved = FALSE
LIMIT 5;

-- Update a submission to approved
UPDATE submissions
SET approved = TRUE
WHERE submission_id = 'eecdabcb-4';

-- Query again to check the status of submissions
SELECT s.submission_id, s.contract_id, s.approved, c.status AS contract_status
FROM submissions s
JOIN contracts c ON s.contract_id = c.contract_id
WHERE s.approved = FALSE
LIMIT 5;

-- Rollback the transaction if necessary
ROLLBACK;
