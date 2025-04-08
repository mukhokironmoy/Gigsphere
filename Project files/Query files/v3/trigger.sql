 --Auto-Set Status to "open" for New Projects
CREATE OR REPLACE FUNCTION set_default_project_status()
RETURNS TRIGGER AS $$
BEGIN
    NEW.status := 'open';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_project_status
BEFORE INSERT ON projects
FOR EACH ROW
EXECUTE FUNCTION set_default_project_status();

INSERT INTO projects (client_id, title, description, budget, deadline)
VALUES ('85d3d266-8', 'New AI Project', 'Develop an AI model', 5000.00, '2025-06-01');

select * from clients
SELECT * FROM projects WHERE title = 'New AI Project';


-- Prevent Users from Changing Their Own user_id
CREATE OR REPLACE FUNCTION prevent_user_id_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.user_id <> NEW.user_id THEN
        RAISE EXCEPTION 'user_id cannot be modified!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_prevent_user_id_change
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION prevent_user_id_change();

UPDATE users SET user_id = '9876543210' WHERE user_id = '85d3d266-8';


--Update Invoice Status When Payment is Made
CREATE OR REPLACE FUNCTION update_invoice_on_payment()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE invoices
    SET status = 'paid', paid_at = CURRENT_TIMESTAMP
    WHERE contract_id = NEW.contract_id AND status = 'pending';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_invoice_status
AFTER INSERT ON payments
FOR EACH ROW
WHEN (NEW.status = 'completed')
EXECUTE FUNCTION update_invoice_on_payment();

select * from contracts

INSERT INTO invoices (invoice_id, contract_id, net_amount, due_date, status)
VALUES ('INV12345', 'c2d90c59-b', 2000.00, '2025-04-15', 'pending');


INSERT INTO payments (payment_id, contract_id, amount, payment_method, status)
VALUES ('PAY12345', 'c2d90c59-b', 2000.00, 'Credit Card', 'completed');


SELECT * FROM invoices WHERE invoice_id = 'INV12345';



--Prevent Freelancers from Bidding Below Their Hourly Rate
CREATE OR REPLACE FUNCTION enforce_minimum_bid()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.bid_amount < (SELECT hourly_rate FROM freelancers WHERE freelancer_id = NEW.freelancer_id) THEN
        RAISE EXCEPTION 'Bid amount cannot be lower than freelancer hourly rate!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_enforce_minimum_bid
BEFORE INSERT ON proposals
FOR EACH ROW
EXECUTE FUNCTION enforce_minimum_bid();

select * from freelancers
select * from projects

INSERT INTO proposals (proposal_id, freelancer_id, project_id, proposal_text, bid_amount)
VALUES ('PROP12345', '2d140e33-c', 'f6c43c7d-e', 'I will complete this task.', 30.00);



