import sqlite3

def create_database():
    conn = sqlite3.connect('amusement_park.db')
    cursor = conn.cursor()

    # สร้างตาราง users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        ticket_id INTEGER)''')

    # สร้างตาราง rides
    cursor.execute('''CREATE TABLE IF NOT EXISTS rides (
                        ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ride_name TEXT NOT NULL,
                        description TEXT,
                        price REAL NOT NULL)''')

    # สร้างตาราง tickets
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ride_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (ride_id) REFERENCES rides(ride_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id))''')

    conn.commit()
    conn.close()

create_database()
