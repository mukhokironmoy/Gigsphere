--TRIGGER FILE



----------------------------------------------------------------------------------------------------------------------------------------

--Trigger for creating client and freelancer from user
CREATE OR REPLACE FUNCTION insert_role_table()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_type = 'client' THEN
        INSERT INTO clients (client_id) VALUES (NEW.user_id);
    ELSIF NEW.user_type = 'freelancer' THEN
        INSERT INTO freelancers (freelancer_id) VALUES (NEW.user_id);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_insert_role_table
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION insert_role_table();

----------------------------------------------------------------------------------------------------------------------------------------

--Trigger for creating an invoice every time a contract is made
CREATE OR REPLACE FUNCTION create_invoice_on_contract_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO invoices (
        contract_id,
        net_amount,
        due_date,
        status
    ) VALUES (
        NEW.contract_id,
        NEW.agreed_price,
        NEW.start_date + INTERVAL '30 days',
        'pending'
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_create_invoice
AFTER INSERT ON contracts
FOR EACH ROW
EXECUTE FUNCTION create_invoice_on_contract_insert();

----------------------------------------------------------------------------------------------------------------------------------------

--Trigger for updating invoice status after payment
CREATE OR REPLACE FUNCTION update_invoice_status_on_payment()
RETURNS TRIGGER AS $$
BEGIN
    -- Only update if the payment is completed
    IF NEW.status = 'completed' THEN
        UPDATE invoices
        SET status = 'paid',
            paid_at = NEW.paid_at
        WHERE invoice_id = NEW.invoice_id;
    END IF;

    -- No action if payment is failed
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_invoice_after_payment
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION update_invoice_status_on_payment();

