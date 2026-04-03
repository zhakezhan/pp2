-- Procedure: insert or update
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- Procedure: bulk insert with validation
CREATE OR REPLACE PROCEDURE bulk_insert_with_report(
    p_names TEXT[], 
    p_phones TEXT[], 
    INOUT p_errors TEXT DEFAULT ''
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    -- Initialize the error string
    p_errors := '';

    -- Loop through the arrays using the length of the names list
    FOR i IN 1..array_length(p_names, 1) LOOP
        
        -- IF check: Validate the format (+ and exactly 11 digits)
        IF p_phones[i] ~ '^\+[0-9]{11}$' THEN
            -- If valid, call your existing single-row logic
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            -- If invalid, add the bad data to our report string
            p_errors := p_errors || 'Error at Row ' || i || ': ' || p_names[i] || ' (' || p_phones[i] || '); ';
            
            -- Optional: Show a notice in the Postgres console
            RAISE NOTICE 'Skipping invalid data: %', p_phones[i];
        END IF;

    END LOOP;
END;
$$;


-- Procedure: delete
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone = p_value;
END;
$$;