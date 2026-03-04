import sqlite3
import re

# Database management
def create_database():
    connection = sqlite3.connect('sim_tracker.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sims (
            id INTEGER PRIMARY KEY,
            phone_number TEXT UNIQUE,
            status TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Phone number validation
def is_valid_number(phone_number):
    pattern = re.compile(r'^\\+?[1-9]\\d{1,14}$')  # E.164 format
    return pattern.match(phone_number)

# SIM status tracking
def add_sim(phone_number, status):
    if not is_valid_number(phone_number):
        print("Invalid phone number.")
        return
    connection = sqlite3.connect('sim_tracker.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO sims (phone_number, status) VALUES (?, ?)', (phone_number, status))
        connection.commit()
    except sqlite3.IntegrityError:
        print("SIM already exists.")
    connection.close()

def update_status(phone_number, status):
    connection = sqlite3.connect('sim_tracker.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE sims SET status = ? WHERE phone_number = ?', (status, phone_number))
    connection.commit()
    connection.close()

# User interface menu system
def menu():
    create_database()
    while True:
        print("\nSIM Tracker Menu")
        print("1. Add SIM")
        print("2. Update SIM Status")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            phone_number = input("Enter phone number: ")
            status = input("Enter SIM status: ")
            add_sim(phone_number, status)
        elif choice == '2':
            phone_number = input("Enter phone number: ")
            status = input("Enter new SIM status: ")
            update_status(phone_number, status)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    menu()