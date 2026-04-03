-- Function: search by pattern
CREATE OR REPLACE FUNCTION search_pattern(p_pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE first_name ILIKE '%' || p_pattern || '%'
       OR phone ILIKE '%' || p_pattern || '%';
END;
$$;


-- Function: pagination
CREATE OR REPLACE FUNCTION get_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    ORDER BY id
    LIMIT limit_val OFFSET offset_val;
END;
$$;