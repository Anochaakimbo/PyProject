import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def register_user(username, password):
    conn = sqlite3.connect(r'C:\Users\user\Downloads\test.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(r'C:\Users\user\Downloads\test.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        return user
    else:
        print("Invalid username or password.")
        return None

def get_user_tickets(user_id):
    conn = sqlite3.connect(r'C:\Users\user\Downloads\test.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.ride_name, r.price 
        FROM tickets t 
        JOIN rides r ON t.ride_id = r.ride_id 
        WHERE t.user_id = ?
    """, (user_id,))
    
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def buy_ticket(user_id, ride_id):
    conn = sqlite3.connect(r'C:\Users\user\Downloads\test.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO tickets (user_id, ride_id) VALUES (?, ?)", (user_id, ride_id))
        conn.commit()
        messagebox.showinfo("Success", "Ticket purchased successfully!")
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to purchase ticket: {str(e)}")
        return False
    finally:
        conn.close()

def show_main_window(user):
    main_window = tk.Tk()
    main_window.title("Amusement Park")
    main_window.geometry("1200x600")

    # Welcome message
    tk.Label(main_window, text=f"Welcome, {user[1]}!", font=("Arial", 16, "bold")).pack(pady=10)

    # Create frames
    left_frame = ttk.Frame(main_window)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

    right_frame = ttk.Frame(main_window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Available rides section
    tk.Label(left_frame, text="Available Rides", font=("Arial", 14, "bold")).pack(pady=5)
    rides_tree = ttk.Treeview(left_frame, columns=("Name", "Description", "Price"), show="headings")
    rides_tree.heading("Name", text="Name")
    rides_tree.heading("Description", text="Description")
    rides_tree.heading("Price", text="Price")
    rides_tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # My tickets section
    tk.Label(right_frame, text="My Tickets", font=("Arial", 14, "bold")).pack(pady=5)
    tickets_tree = ttk.Treeview(right_frame, columns=("Ride", "Price"), show="headings")
    tickets_tree.heading("Ride", text="Ride")
    tickets_tree.heading("Price", text="Price")
    tickets_tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def refresh_rides():
        rides_tree.delete(*rides_tree.get_children())
        conn = sqlite3.connect(r'C:\Users\user\Downloads\test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rides")
        rides = cursor.fetchall()
        conn.close()

        for ride in rides:
            rides_tree.insert("", tk.END, values=ride)

    def refresh_tickets():
        tickets_tree.delete(*tickets_tree.get_children())
        tickets = get_user_tickets(user[0])
        for ticket in tickets:
            tickets_tree.insert("", tk.END, values=ticket)

    def purchase_ticket():
        selected_item = rides_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a ride first!")
            return

        ride_id = rides_tree.item(selected_item)['values'][0]
        if buy_ticket(user[0], ride_id):
            refresh_tickets()

    # Purchase button
    tk.Button(left_frame, text="Purchase Selected Ride", command=purchase_ticket).pack(pady=10)

    # Initial data load
    refresh_rides()
    refresh_tickets()

    main_window.mainloop()

def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Login", "Login successful!")
            login_window.destroy()
            show_main_window(user)
        else:
            messagebox.showerror("Login", "Invalid username or password")

    tk.Button(login_window, text="Login", command=login).pack(pady=10)
    tk.Button(login_window, text="Register", command=lambda: show_register_window()).pack()

    login_window.mainloop()

def show_register_window():
    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry("300x200")

    tk.Label(register_window, text="Username").pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    tk.Label(register_window, text="Password").pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        register_user(username, password)
        messagebox.showinfo("Register", "Registration successful!")
        register_window.destroy()

    tk.Button(register_window, text="Register", command=register).pack(pady=10)

    register_window.mainloop()

# Start the application
if __name__ == "__main__":
    show_login_window()