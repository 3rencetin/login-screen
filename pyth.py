import tkinter as tk
from tkinter import messagebox
import sqlite3

# SQLite veritabanına bağlanma veya oluşturma
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Kullanıcılar tablosunu oluşturma (Eğer yoksa)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')

# Dashboard tablosunu oluşturma (Eğer yoksa)
cursor.execute('''CREATE TABLE IF NOT EXISTS dashboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    info TEXT)''')

conn.commit()

def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def register_screen():
    def register():
        username = register_username.get()
        password = register_password.get()
        confirm = confirm_password.get()

        if password == confirm:
            if register_user(username, password):
                messagebox.showinfo("Register", "Registration Successful!")
                register_window.destroy()
            else:
                messagebox.showerror("Register", "Username already exists!")
        else:
            messagebox.showerror("Register", "Passwords do not match!")

    register_window = tk.Toplevel(app)
    register_window.title("Register")
    register_window.geometry("300x300")
    register_window.resizable(False, False)
    
    tk.Label(register_window, text="Register", font=("Helvetica", 14, "bold")).pack(pady=10)
    
    tk.Label(register_window, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    register_username = tk.Entry(register_window, font=("Helvetica", 12))
    register_username.pack()
    
    tk.Label(register_window, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    register_password = tk.Entry(register_window, show="*", font=("Helvetica", 12))
    register_password.pack()
    
    tk.Label(register_window, text="Confirm Password:", font=("Helvetica", 12)).pack(pady=5)
    confirm_password = tk.Entry(register_window, show="*", font=("Helvetica", 12))
    confirm_password.pack()
    
    tk.Button(register_window, text="Register", command=register, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

def open_dashboard():
    def fetch_dashboard_data():
        cursor.execute("SELECT * FROM dashboard")
        data = cursor.fetchall()
        return data
    
    dashboard_window = tk.Toplevel(app)
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("500x400")
    dashboard_window.resizable(False, False)
    
    tk.Label(dashboard_window, text="Dashboard", font=("Helvetica", 14, "bold")).pack(pady=10)
    
    data = fetch_dashboard_data()
    if data:
        tk.Label(dashboard_window, text="Information:", font=("Helvetica", 12, "bold")).pack()
        for item in data:
            tk.Label(dashboard_window, text=f"Username: {item[1]}, Info: {item[2]}").pack()
        tk.Label(dashboard_window, text="").pack()  # Boşluk ekleyelim
    else:
        tk.Label(dashboard_window, text="No information available", font=("Helvetica", 12, "italic")).pack()

    tk.Button(dashboard_window, text="Open Custom Page", command=open_custom_page, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white").pack(pady=20)
    
    tk.Button(dashboard_window, text="Close", command=dashboard_window.destroy, font=("Helvetica", 12, "bold"), bg="#f44336", fg="white").pack(pady=20)

def add_info_to_dashboard(username, info):
    try:
        cursor.execute("INSERT INTO dashboard (username, info) VALUES (?, ?)", (username, info))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error inserting data into dashboard: {e}")
        return False

def open_custom_page():
    custom_page = tk.Toplevel()
    custom_page.title("Custom Page")
    custom_page.geometry("600x400")
    
    label = tk.Label(custom_page, text="Eren'in Dünyasına Hoşgeldiniz", font=("Helvetica", 24, "bold"))
    label.pack(pady=50)
    
    custom_page.mainloop()

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    
    if result:
        messagebox.showinfo("Login", "Login Successful!")
        add_info_to_dashboard(username, "Logged in successfully.")
        open_dashboard()
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

# Ana pencereyi oluştur
app = tk.Tk()
app.title("Login Screen")
app.geometry("300x300")
app.resizable(False, False)

# Üst bilgi (header) etiketi
header_label = tk.Label(app, text="Welcome! Please Login", font=("Helvetica", 14, "bold"))
header_label.pack(pady=10)

# Kullanıcı adı etiketi ve giriş kutusu
frame_username = tk.Frame(app)
frame_username.pack(pady=5)

label_username = tk.Label(frame_username, text="Username:", font=("Helvetica", 12))
label_username.pack(side=tk.LEFT, padx=5)

entry_username = tk.Entry(frame_username, font=("Helvetica", 12))
entry_username.pack(side=tk.LEFT)

# Şifre etiketi ve giriş kutusu
frame_password = tk.Frame(app)
frame_password.pack(pady=5)

label_password = tk.Label(frame_password, text="Password:", font=("Helvetica", 12))
label_password.pack(side=tk.LEFT, padx=5)

entry_password = tk.Entry(frame_password, show="*", font=("Helvetica", 12))
entry_password.pack(side=tk.LEFT)

# Giriş butonu
login_button = tk.Button(app, text="Login", command=login, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
login_button.pack(pady=10)

# Kayıt butonu
register_button = tk.Button(app, text="Register", command=register_screen, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white")
register_button.pack(pady=10)

# Ana döngüyü başlat
app.mainloop()

# Uygulama kapatıldığında veritabanı bağlantısını kapat
conn.close()
