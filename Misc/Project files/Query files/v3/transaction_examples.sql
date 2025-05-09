-- Create a user (client)
INSERT INTO users (user_id, username, email, user_type, password_hash)
VALUES ('USRCLIENT1', 'client_user', 'client@example.com', 'client', 'hashed_pwd');

-- Create a user (freelancer)
INSERT INTO users (user_id, username, email, user_type, password_hash)
VALUES ('USRFREE001', 'freelancer_user', 'freelancer@example.com', 'freelancer', 'hashed_pwd');

-- Insert client and freelancer
INSERT INTO clients (client_id, company_name, business_type)
VALUES ('USRCLIENT1', 'TechCorp', 'IT Services');

INSERT INTO freelancers (freelancer_id, bio, portfolio, experience, hourly_rate)
VALUES ('USRFREE001', 'Experienced developer', 'portfolio.com', 5, 50.00);

-- Create a project
INSERT INTO projects (project_id, client_id, title, description, budget, deadline, status)
VALUES ('PROJ000001', 'USRCLIENT1', 'Build Web App', 'A full-stack project', 5000.00, '2025-12-31', 'open');

-- Create a proposal
INSERT INTO proposals (proposal_id, freelancer_id, project_id, proposal_text, bid_amount)
VALUES ('PROP000001', 'USRFREE001', 'PROJ000001', 'I will build your app.', 4800.00);

-- Create a contract
INSERT INTO contracts (contract_id, client_id, freelancer_id, project_id, proposal_id, agreed_price, start_date, status)
VALUES ('CONT000001', 'USRCLIENT1', 'USRFREE001', 'PROJ000001', 'PROP000001', 4800.00, '2025-04-25', 'active');



BEGIN;

-- Set contract to completed
UPDATE contracts SET status = 'completed' WHERE contract_id = 'CONT000001';

-- Savepoint before inserting payment
SAVEPOINT before_payment;

-- Faulty insert (violates amount >= 0)
INSERT INTO payments (payment_id, contract_id, amount, payment_method, status)
VALUES ('PAY0000001', 'CONT000001', -200.00, 'Card', 'completed');

-- Rollback to recover from error
ROLLBACK TO SAVEPOINT before_payment;

-- Correct payment
INSERT INTO payments (payment_id, contract_id, amount, payment_method, status)
VALUES ('PAY0000001', 'CONT000001', 200.00, 'Card', 'completed');

COMMIT;


BEGIN;

-- Set contract to completed
UPDATE contracts SET status = 'completed' WHERE contract_id = 'CONT000001';

-- Savepoint before inserting payment
SAVEPOINT before_payment;

-- Faulty insert (violates amount >= 0)
INSERT INTO payments (payment_id, contract_id, amount, payment_method, status)
VALUES ('PAY0000001', 'CONT000001', -200.00, 'Card', 'completed');

-- Rollback to recover from error
ROLLBACK TO SAVEPOINT before_payment;

-- Correct payment
INSERT INTO payments (payment_id, contract_id, amount, payment_method, status)
VALUES ('PAY0000001', 'CONT000001', 200.00, 'Card', 'completed');

COMMIT;


BEGIN;

-- Only allow invoice if contract is completed
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contracts WHERE contract_id = 'CONT000001' AND status = 'completed'
    ) THEN
        INSERT INTO invoices (invoice_id, contract_id, net_amount, due_date, status)
        VALUES ('INV0000001', 'CONT000001', 200.00, '2025-05-01', 'pending');
    ELSE
        RAISE NOTICE 'Contract is not completed. Invoice not issued.';
    END IF;
END$$;

COMMIT;


BEGIN;

-- Lock the contract row
SELECT * FROM contracts
WHERE contract_id = 'CONT000001'
FOR UPDATE;

-- Update price and status
UPDATE contracts
SET agreed_price = 5000.00, status = 'completed'
WHERE contract_id = 'CONT000001';

COMMIT;


BEGIN;

-- Attempt to insert a withdrawal with same user as requester and approver
INSERT INTO withdrawals (withdrawal_id, requested_by, approved_by, contract_id, reason, status)
VALUES ('WDRAW00001', 'USRCLIENT1', 'USRCLIENT1', 'CONT000001', 'Duplicate payment', 'pending');

-- Realize we made a logic error → rollback everything
ROLLBACK;



