import csv
from connect import connect

# Создание таблицы
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

# Вставка контактов из CSV
def insert_from_csv(filename='contacts.csv'):
    sql = "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (first_name, phone) DO NOTHING"
    conn = connect()
    cur = conn.cursor()
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(sql, (row['first_name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported successfully!")

# Вставка контакта вручную
def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    sql = "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (first_name, phone) DO NOTHING"
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, (first_name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Contact '{first_name}' added successfully.")

# Обновление контакта
def update_contact():
    search_all()
    contact_id = input("Enter the ID of contact to update: ")
    print("1 - Update name")
    print("2 - Update phone number")
    choice = input("Choose 1 or 2: ")
    conn = connect()
    cur = conn.cursor()
    if choice == '1':
        new_name = input("Enter new name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE id = %s", (new_name, contact_id))
        print("Name updated.")
    elif choice == '2':
        new_phone = input("Enter new phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s", (new_phone, contact_id))
        print("Phone updated.")
    else:
        print("Invalid choice.")
    conn.commit()
    cur.close()
    conn.close()

# Показать все контакты
def search_all():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")
    print("-"*45)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
    cur.close()
    conn.close()

# Поиск по имени
def search_by_name():
    name = input("Enter name to search: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + name + '%',))
    rows = cur.fetchall()
    print(f"Results for '{name}':")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
    cur.close()
    conn.close()

# Поиск по префиксу номера
def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE LEFT(phone, %s) = %s", (len(prefix), prefix))
    rows = cur.fetchall()
    print(f"Results for prefix '{prefix}':")
    print(f"{'ID':<5} {'Name':<20} {'Phone':<20}")
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
    cur.close()
    conn.close()

# Удаление контакта
def delete_by_name():
    name = input("Enter name to delete: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    print(f"Deleted {deleted} contact(s) with name '{name}'.")

# Главное меню
def main():
    create_table()
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Import contacts from CSV")
        print("2. Add contact manually")
        print("3. Update a contact")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Search by phone prefix")
        print("7. Delete by name")
        print("0. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            search_all()
        elif choice == '5':
            search_by_name()
        elif choice == '6':
            search_by_phone_prefix()
        elif choice == '7':
            delete_by_name()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()