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
CREATE OR REPLACE PROCEDURE bulk_insert(names TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        IF phones[i] ~ '^[0-9]+$' THEN
            CALL upsert_contact(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', phones[i];
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