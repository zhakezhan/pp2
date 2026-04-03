import csv
from connect import connect

# Create phonebook table
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) UNIQUE,
        phone VARCHAR(20) UNIQUE
    )
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


# Insert contacts from CSV using procedure (upsert)
def insert_from_csv(filename="contacts.csv"):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "CALL upsert_contact(%s, %s)",
                    (row['first_name'], row['phone'])
                )

        conn.commit()
        print("Contacts imported successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# Insert or update contact manually using procedure
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved (insert/update).")


# Show all contacts
def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")
    print("-" * 45)

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")

    cur.close()
    conn.close()


# Search contacts using function (pattern search)
def search_pattern():
    pattern = input("Enter search text: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    print(f"\nResults for '{pattern}':")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")

    cur.close()
    conn.close()


# Show contacts with pagination using function
def pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    print(f"\nPage (limit={limit}, offset={offset})")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")

    cur.close()
    conn.close()


# Delete contact by name or phone using procedure
def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted.")


# Insert many contacts using procedure (bulk insert with validation)
def bulk_insert():
    names = input("Enter names (comma separated): ").split(',')
    phones = input("Enter phones (comma separated): ").split(',')

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL bulk_insert(%s, %s)", (names, phones))

    conn.commit()
    cur.close()
    conn.close()

    print("Bulk insert completed (invalid phones will be shown as NOTICE).")


# Main menu
def main():
    create_table()

    while True:
        print("\nPHONEBOOK MENU")
        print("1. Import from CSV")
        print("2. Add or update contact")
        print("3. Show all contacts")
        print("4. Search by pattern")
        print("5. Pagination")
        print("6. Delete contact")
        print("7. Bulk insert")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            show_all()
        elif choice == '4':
            search_pattern()
        elif choice == '5':
            pagination()
        elif choice == '6':
            delete_contact()
        elif choice == '7':
            bulk_insert()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()