
-- Drop existing objects
DROP FUNCTION  IF EXISTS get_contacts_by_pattern(text);
DROP FUNCTION  IF EXISTS get_contacts_paginated(int, int);
DROP FUNCTION  IF EXISTS search_contacts(text);
DROP PROCEDURE IF EXISTS upsert_contact(text, text, text, text);
DROP PROCEDURE IF EXISTS delete_contact(text);
DROP PROCEDURE IF EXISTS bulk_insert_contacts(text[], text[], text[]);
DROP PROCEDURE IF EXISTS add_phone(varchar, varchar, varchar);
DROP PROCEDURE IF EXISTS move_to_group(varchar, varchar);


-- 1. Pattern search (name / phone)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_term TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.first_name, c.last_name, p.phone
    FROM phonebook c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || search_term || '%'
       OR c.last_name  ILIKE '%' || search_term || '%'
       OR p.phone      ILIKE '%' || search_term || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Paginated query (LIMIT / OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name
    FROM phonebook c
    ORDER BY c.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


-- 3. Upsert contact (insert or update by name)
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first TEXT,
    p_last  TEXT,
    p_phone TEXT,
    p_type  TEXT DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id
    FROM phonebook
    WHERE first_name ILIKE p_first;

    IF v_id IS NOT NULL THEN
        -- Update existing phone or insert new one
        UPDATE phones SET phone = p_phone
        WHERE contact_id = v_id AND type = p_type;
        IF NOT FOUND THEN
            -- Only insert if phone doesn't already exist
            IF NOT EXISTS (SELECT 1 FROM phones WHERE phone = p_phone) THEN
                INSERT INTO phones (contact_id, phone, type)
                VALUES (v_id, p_phone, p_type);
            END IF;
        END IF;
    ELSE
        INSERT INTO phonebook (first_name, last_name)
        VALUES (p_first, p_last)
        RETURNING id INTO v_id;

        IF NOT EXISTS (SELECT 1 FROM phones WHERE phone = p_phone) THEN
            INSERT INTO phones (contact_id, phone, type)
            VALUES (v_id, p_phone, p_type);
        END IF;
    END IF;
END;
$$;


-- 4. Delete contact by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name ILIKE p_identifier
       OR last_name  ILIKE p_identifier
       OR id IN (
           SELECT contact_id FROM phones WHERE phone = p_identifier
       );
END;
$$;


-- 5. Bulk insert with phone validation
--    Skips rows with duplicate names or invalid/duplicate phones
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    names_first TEXT[],
    names_last  TEXT[],
    phones_arr  TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i    INT;
    v_id INTEGER;
BEGIN
    FOR i IN 1 .. array_upper(names_first, 1) LOOP
        -- Skip invalid phone format
        IF phones_arr[i] !~ '^[0-9]{11}$' THEN
            RAISE NOTICE 'Invalid phone for %: %', names_first[i], phones_arr[i];
            CONTINUE;
        END IF;

        -- Skip duplicate name
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name ILIKE names_first[i]) THEN
            RAISE NOTICE 'Duplicate name skipped: %', names_first[i];
            CONTINUE;
        END IF;

        -- Skip duplicate phone
        IF EXISTS (SELECT 1 FROM phones WHERE phone = phones_arr[i]) THEN
            RAISE NOTICE 'Duplicate phone skipped for %: %', names_first[i], phones_arr[i];
            CONTINUE;
        END IF;

        INSERT INTO phonebook (first_name, last_name)
        VALUES (names_first[i], names_last[i])
        RETURNING id INTO v_id;

        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_id, phones_arr[i], 'mobile');
    END LOOP;
END;
$$;


-- 6. Add phone to existing contact
--    Raises error if contact not found or phone already exists
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id
    FROM phonebook
    WHERE first_name ILIKE p_contact_name
    LIMIT 1;

    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    IF EXISTS (SELECT 1 FROM phones WHERE phone = p_phone) THEN
        RAISE EXCEPTION 'Phone "%" already exists', p_phone;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;


-- 7. Move contact to group (creates group if not exists)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Create group if it doesn't exist
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    SELECT id INTO v_contact_id
    FROM phonebook
    WHERE first_name ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    UPDATE phonebook SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


-- 8. Extended search — matches name, email, and all phone numbers
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id         INT,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    grp        VARCHAR,
    phones     TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS grp,
        STRING_AGG(p.phone || ' (' || COALESCE(p.type, '?') || ')', ', ') AS phones
    FROM phonebook c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name  ILIKE '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR p.phone      ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
END;
$$ LANGUAGE plpgsql;