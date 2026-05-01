import csv
import json
from connect import connect

PAGE_SIZE = 5


#  Display helpers 

def _print_rows(rows, headers):
    if not rows:
        print("  No data found.")
        return
    widths = [
        max(len(str(h)), max((len(str(r[i])) if r[i] is not None else 0) for r in rows))
        for i, h in enumerate(headers)
    ]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print()
    print(fmt.format(*headers))
    print("  ".join("─" * w for w in widths))
    for row in rows:
        print(fmt.format(*[str(v) if v is not None else "" for v in row]))
    print()


def _show_groups(cur):
    cur.execute("SELECT id, name FROM groups ORDER BY name")
    print("\nAvailable groups:")
    for gid, gname in cur.fetchall():
        print(f"  {gid}. {gname}")


def _get_group_id(cur, group_name):
    if not group_name:
        return None
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    return row[0] if row else None


#  Duplicate checks 

def _name_exists(cur, first_name):
    """Return contact id if first_name already exists, else None."""
    cur.execute(
        "SELECT id FROM phonebook WHERE first_name ILIKE %s", (first_name,)
    )
    row = cur.fetchone()
    return row[0] if row else None


def _phone_exists(cur, phone):
    """Return True if phone already exists in phones table."""
    cur.execute("SELECT id FROM phones WHERE phone = %s", (phone,))
    return cur.fetchone() is not None


#  Phone input helper 

def _add_phones(cur, contact_id):
    """Prompt user to add phone numbers. Skips duplicates. Empty input stops."""
    print("Add phone numbers (press Enter with no input to finish):")
    while True:
        phone = input("  Phone number: ").strip()
        if not phone:
            break
        if _phone_exists(cur, phone):
            print(f"  Phone {phone} already exists — skipped.")
            continue
        print("  Type: (1) mobile  (2) home  (3) work")
        ptype = {"1": "mobile", "2": "home", "3": "work"}.get(
            input("  Choice [1]: ").strip(), "mobile"
        )
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )


def _collect_group(cur):
    """Show groups and return chosen group_id or None."""
    _show_groups(cur)
    gid_input = input("Group ID (Enter to skip): ").strip()
    if gid_input.isdigit():
        cur.execute("SELECT id FROM groups WHERE id = %s", (gid_input,))
        row = cur.fetchone()
        return row[0] if row else None
    return None


#  Table creation 

def create_tables():
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    """)
    cur.execute("""
        INSERT INTO groups (name) VALUES ('Family'),('Work'),('Friend'),('Other')
        ON CONFLICT (name) DO NOTHING
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL UNIQUE,
            last_name  VARCHAR(100),
            email      VARCHAR(100),
            birthday   DATE,
            group_id   INTEGER REFERENCES groups(id),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id         SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
            phone      VARCHAR(20) NOT NULL UNIQUE,
            type       VARCHAR(10) CHECK (type IN ('home','work','mobile'))
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


#  CSV import 

def insert_from_csv(filename='contacts.csv'):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    imported = 0
    skipped  = 0

    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                first = row.get('first_name', '').strip()
                last  = row.get('last_name',  '').strip() or None
                email = row.get('email',       '').strip() or None
                bday  = row.get('birthday',    '').strip() or None
                group = row.get('group',       '').strip()
                phone = row.get('phone',       '').strip()
                ptype = row.get('phone_type',  'mobile').strip()

                if not first:
                    continue

                if _name_exists(cur, first):
                    print(f"  Skipped (name exists): {first}")
                    skipped += 1
                    continue

                if phone and _phone_exists(cur, phone):
                    print(f"  Skipped (phone exists — {phone}): {first}")
                    skipped += 1
                    continue

                group_id = _get_group_id(cur, group)
                cur.execute("""
                    INSERT INTO phonebook (first_name, last_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (first, last, email, bday, group_id))
                contact_id = cur.fetchone()[0]

                if phone:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, phone, ptype)
                    )
                imported += 1

        conn.commit()
        print(f"Imported {imported} contact(s). Skipped {skipped} duplicate(s).")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    finally:
        cur.close()
        conn.close()


#  Console add 

def insert_from_console():
    print("\n Add New Contact ")
    first = input("First name (required): ").strip()
    if not first:
        print("First name cannot be empty.")
        return

    last  = input("Last name  (Enter to skip): ").strip() or None
    email = input("Email      (Enter to skip): ").strip() or None
    bday  = input("Birthday YYYY-MM-DD (Enter to skip): ").strip() or None

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()

    existing_id = _name_exists(cur, first)
    if existing_id:
        print(f"\n  Contact '{first}' already exists.")
        choice = input("  (s) skip  (o) overwrite > ").strip().lower()
        if choice != 'o':
            print("  Skipped.")
            cur.close(); conn.close(); return

        group_id = _collect_group(cur)
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing_id,))
        cur.execute("""
            UPDATE phonebook
            SET last_name=%s, email=%s, birthday=%s, group_id=%s
            WHERE id=%s
        """, (last, email, bday, group_id, existing_id))
        contact_id = existing_id
        print(f"  Overwriting '{first}'...")
    else:
        group_id = _collect_group(cur)
        cur.execute("""
            INSERT INTO phonebook (first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (first, last, email, bday, group_id))
        contact_id = cur.fetchone()[0]

    _add_phones(cur, contact_id)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Contact '{first}' saved.")


#  Show all 

def show_all():
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email,
               c.birthday::text, g.name,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, g.name
        ORDER BY c.first_name
    """)
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Birthday","Group","Phones"])
    cur.close()
    conn.close()


#  Update 

def update_contact():
    show_all()
    cid = input("Enter ID to update: ").strip()
    if not cid.isdigit():
        print("Invalid ID.")
        return

    print("""
What to update?
  1. First name
  2. Last name
  3. Email
  4. Birthday
  5. Group
  6. Add phone number
  7. Update existing phone number
""")
    choice = input("Choice: ").strip()

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()

    if choice == '1':
        val = input("New first name: ").strip()
        cur.execute(
            "SELECT id FROM phonebook WHERE first_name ILIKE %s AND id != %s", (val, cid)
        )
        if cur.fetchone():
            print(f"  Name '{val}' already taken — cancelled.")
            cur.close(); conn.close(); return
        cur.execute("UPDATE phonebook SET first_name = %s WHERE id = %s", (val, cid))
    elif choice == '2':
        val = input("New last name: ").strip()
        cur.execute("UPDATE phonebook SET last_name = %s WHERE id = %s", (val, cid))
    elif choice == '3':
        val = input("New email: ").strip()
        cur.execute("UPDATE phonebook SET email = %s WHERE id = %s", (val, cid))
    elif choice == '4':
        val = input("Birthday YYYY-MM-DD: ").strip()
        cur.execute("UPDATE phonebook SET birthday = %s WHERE id = %s", (val, cid))
    elif choice == '5':
        _show_groups(cur)
        gid = input("Group ID: ").strip()
        cur.execute("UPDATE phonebook SET group_id = %s WHERE id = %s", (gid, cid))
    elif choice == '6':
        phone = input("Phone number: ").strip()
        if _phone_exists(cur, phone):
            print(f"  Phone {phone} already exists — cancelled.")
            cur.close(); conn.close(); return
        print("Type: (1) mobile  (2) home  (3) work")
        ptype = {"1": "mobile", "2": "home", "3": "work"}.get(
            input("Choice [1]: ").strip(), "mobile"
        )
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (cid, phone, ptype)
        )
    elif choice == '7':

            # 1. Show existing phones for this contact
            cur.execute("SELECT id, phone, type FROM phones WHERE contact_id = %s", (cid,))
            phones = cur.fetchall()
            
            if not phones:
                print("No phone numbers found for this contact.")
                return

            print("\nSelect phone to update:")
            for i, (pid, pnum, ptyp) in enumerate(phones):
                print(f"  {i+1}. {pnum} ({ptyp})")
            
            idx_input = input("Choice: ").strip()
            if not idx_input.isdigit() or not (1 <= int(idx_input) <= len(phones)):
                print("Invalid selection.")
                return
            
            target_phone_id = phones[int(idx_input) - 1][0]
            
            # 2. Get new data
            new_phone = input("Enter new phone number: ").strip()
            
            # Check if the new number is already used by someone else
            cur.execute("SELECT id FROM phones WHERE phone = %s AND id != %s", (new_phone, target_phone_id))
            if cur.fetchone():
                print(f"  Phone {new_phone} is already taken — cancelled.")
                return

            print("New Type: (1) mobile  (2) home  (3) work")
            new_type = {"1": "mobile", "2": "home", "3": "work"}.get(
                input("Choice [1]: ").strip(), "mobile"
            )

            # 3. Execute Update
            cur.execute(
                "UPDATE phones SET phone = %s, type = %s WHERE id = %s",
                (new_phone, new_type, target_phone_id)
            )
    else:
        print("Invalid choice.")
        cur.close(); conn.close(); return

    conn.commit()
    cur.close()
    conn.close()
    print("Updated successfully.")


#  Search / Filter ─

def search_by_name():
    name = input("Enter name: ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday::text,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.first_name ILIKE %s OR c.last_name ILIKE %s
        GROUP BY c.id
        ORDER BY c.first_name
    """, (f'%{name}%', f'%{name}%'))
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Birthday","Phones"])
    cur.close()
    conn.close()


def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, p.phone, p.type
        FROM phonebook c
        JOIN phones p ON p.contact_id = c.id
        WHERE p.phone LIKE %s
        ORDER BY c.first_name
    """, (prefix + '%',))
    _print_rows(cur.fetchall(), ["ID","First","Last","Phone","Type"])
    cur.close()
    conn.close()


def filter_by_group():
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    _show_groups(cur)
    gid = input("Enter group ID: ").strip()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday::text,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.group_id = %s
        GROUP BY c.id
        ORDER BY c.first_name
    """, (gid,))
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Birthday","Phones"])
    cur.close()
    conn.close()


def search_by_email():
    query = input("Enter email fragment: ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.email ILIKE %s
        GROUP BY c.id
        ORDER BY c.first_name
    """, (f'%{query}%',))
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Phones"])
    cur.close()
    conn.close()


def list_sorted():
    print("\nSort by: (1) Name  (2) Birthday  (3) Date added")
    choice = input("Choice: ").strip()
    order = {"1": "c.first_name", "2": "c.birthday", "3": "c.created_at"}.get(
        choice, "c.first_name"
    )
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday::text, g.name,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, g.name
        ORDER BY {order} NULLS LAST
    """)
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Birthday","Group","Phones"])
    cur.close()
    conn.close()


#  Delete 

def delete_by_name():
    name = input("Enter name to delete: ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name ILIKE %s", (name,))
    conn.commit()
    print(f"Deleted {cur.rowcount} contact(s).")
    cur.close()
    conn.close()


#  Pagination 

def paginated_browse():
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM phonebook")
    total = cur.fetchone()[0]

    if total == 0:
        print("No contacts found.")
        cur.close(); conn.close(); return

    page = 0
    total_pages = -(-total // PAGE_SIZE)

    while True:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (PAGE_SIZE, page * PAGE_SIZE)
        )
        rows = cur.fetchall()
        print(f"\n  Page {page + 1} of {total_pages}")
        _print_rows(rows, ["ID","First","Last"])

        nav = []
        if page > 0:
            nav.append("(p) prev")
        if page + 1 < total_pages:
            nav.append("(n) next")
        nav.append("(q) quit")

        cmd = input(" | ".join(nav) + "  > ").strip().lower()
        if cmd == 'n' and page + 1 < total_pages:
            page += 1
        elif cmd == 'p' and page > 0:
            page -= 1
        elif cmd == 'q':
            break

    cur.close()
    conn.close()


#  JSON export / import 

def export_json(filename='contacts_export.json'):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday::text, g.name
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.first_name
    """)
    contacts = []
    for cid, first, last, email, bday, grp in cur.fetchall():
        cur2 = conn.cursor()
        cur2.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
        phones = [{"phone": ph, "type": t} for ph, t in cur2.fetchall()]
        cur2.close()
        contacts.append({
            "first_name": first,
            "last_name":  last,
            "email":      email,
            "birthday":   bday,
            "group":      grp,
            "phones":     phones
        })
    cur.close()
    conn.close()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(contacts)} contact(s) to '{filename}'.")


def import_json(filename='contacts_export.json'):
    try:
        with open(filename, encoding='utf-8') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()

    for c in contacts:
        first = c.get('first_name', '').strip()
        if not first:
            continue

        existing_id = _name_exists(cur, first)
        if existing_id:
            choice = input(f"'{first}' already exists. (s)kip / (o)verwrite? ").strip().lower()
            if choice != 'o':
                print(f"  Skipped: {first}")
                continue
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing_id,))
            group_id = _get_group_id(cur, c.get('group'))
            cur.execute("""
                UPDATE phonebook
                SET last_name=%s, email=%s, birthday=%s, group_id=%s
                WHERE id=%s
            """, (c.get('last_name'), c.get('email'), c.get('birthday'), group_id, existing_id))
            contact_id = existing_id
        else:
            group_id = _get_group_id(cur, c.get('group'))
            cur.execute("""
                INSERT INTO phonebook (first_name, last_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (first, c.get('last_name'), c.get('email'), c.get('birthday'), group_id))
            contact_id = cur.fetchone()[0]

        for ph in c.get('phones', []):
            phone = ph.get('phone', '').strip()
            if not phone:
                continue
            if _phone_exists(cur, phone):
                print(f"  Phone {phone} already exists — skipped.")
                continue
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, phone, ph.get('type', 'mobile'))
            )

        conn.commit()
        print(f"  Saved: {first}")

    cur.close()
    conn.close()
    print("JSON import complete.")


#  Stored procedure callers 

def call_add_phone():
    name  = input("Contact first name: ").strip()
    phone = input("Phone number: ").strip()

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()

    if _phone_exists(cur, phone):
        print(f"  Phone {phone} already exists — cancelled.")
        cur.close(); conn.close(); return

    print("Type: (1) mobile  (2) home  (3) work")
    ptype = {"1": "mobile", "2": "home", "3": "work"}.get(
        input("Choice [1]: ").strip(), "mobile"
    )
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def call_move_to_group():
    name  = input("Contact first name: ").strip()
    group = input("Group name: ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"'{name}' moved to group '{group}'.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


def call_search_contacts():
    query = input("Search (name / email / phone): ").strip()
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    _print_rows(cur.fetchall(), ["ID","First","Last","Email","Birthday","Group","Phones"])
    cur.close()
    conn.close()


#  Menu 

MENU = """
╔═════════════════════════════════════════╗
║          PhoneBook  —  TSIS 1           ║
╠═════════════════════════════════════════╣
║  1.  Import CSV                         ║
║  2.  Add contact                        ║
║  3.  Update contact                     ║
║  4.  Show all                           ║
║  5.  Search by name                     ║
║  6.  Search by phone prefix             ║
║  7.  Delete by name                     ║
╠═════════════════════════════════════════╣
║  8.  Filter by group                    ║
║  9.  Search by email                    ║
║  10. Show all (sorted)                  ║
║  11. Browse pages                       ║
║  12. Export to JSON                     ║
║  13. Import from JSON                   ║
║  14. Add phone to contact               ║
║  15. Move contact to group              ║
║  16. Extended search                    ║
╠═════════════════════════════════════════╣
║  0.  Exit                               ║
╚═════════════════════════════════════════╝"""


def main():
    create_tables()

    actions = {
        '1':  insert_from_csv,
        '2':  insert_from_console,
        '3':  update_contact,
        '4':  show_all,
        '5':  search_by_name,
        '6':  search_by_phone_prefix,
        '7':  delete_by_name,
        '8':  filter_by_group,
        '9':  search_by_email,
        '10': list_sorted,
        '11': paginated_browse,
        '12': export_json,
        '13': import_json,
        '14': call_add_phone,
        '15': call_move_to_group,
        '16': call_search_contacts,
    }

    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice == '0':
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()