import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from datetime import datetime
import sqlite3

# Database setup
conn = sqlite3.connect('player_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    username TEXT PRIMARY KEY,
    password TEXT,
    membership TEXT DEFAULT 'Junior',
    games_played INTEGER DEFAULT 0,
    win_rate REAL DEFAULT 0,
    days_used INTEGER DEFAULT 0,
    is_admin INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS activation_codes (
    username TEXT,
    script_name TEXT,
    activation_code TEXT,
    PRIMARY KEY (username, script_name)
)
''')

conn.commit()

# Scripts
scripts = {
    "Junior": "Basic Script",
    "Intermediate": "Advanced Script",
    "Premium": "Elite Script"
}

class Player:
    def __init__(self, username, password, membership="Junior", games_played=0, win_rate=0, days_used=0, is_admin=0):
        self.username = username
        self.password = password
        self.membership = membership
        self.games_played = games_played
        self.win_rate = win_rate
        self.days_used = days_used
        self.script = scripts[membership]
        self.is_script_activated = False  # Track if the script is activated
        self.is_admin = is_admin

    def upgrade_membership(self):
        if self.games_played >= 50 and self.days_used >= 30 and self.membership == "Junior":
            self.membership = "Intermediate"
            self.script = scripts["Intermediate"]
        elif self.games_played >= 100 and self.days_used >= 15 and self.membership == "Intermediate":
            self.membership = "Premium"
            self.script = scripts["Premium"]

    def check_activation_code(self, code):
        cursor.execute('SELECT activation_code FROM activation_codes WHERE username = ? AND script_name = ?', (self.username, self.script))
        result = cursor.fetchone()
        if result and result[0] == code:
            self.is_script_activated = True
            return True
        return False

    def get_script(self):
        return self.script if self.is_script_activated else "Script not activated"

class BattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Simulation")
        self.current_player = None

        # Menu Bar (Horizontal)
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Menu Options
        menu_options = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_options)
        menu_options.add_command(label="Log In", command=self.login)
        menu_options.add_command(label="Signup", command=self.signup)
        menu_options.add_separator()
        menu_options.add_command(label="Start 6v6 Battle", command=self.start_6v6_battle)
        menu_options.add_command(label="Start 3v3 Battle", command=self.start_3v3_battle)
        menu_options.add_command(label="Activate Script", command=self.activate_script)
        menu_options.add_command(label="Tasks", command=self.show_tasks)
        menu_options.add_command(label="Advertising", command=self.show_advertising)

        # Admin Menu Option
        menu_options.add_command(label="Admin Panel", command=self.show_admin_panel)

        # Login Frame
        self.login_frame = tk.Frame(root, bg="lightblue")
        self.login_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(self.login_frame, text="Username", bg="lightblue").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.login_frame, text="Password", bg="lightblue").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2)

        # Battle & Stats Frame
        self.battle_frame = tk.Frame(root)
        self.battle_frame.pack(padx=10, pady=10)
        self.battle_left_frame = tk.Frame(self.battle_frame, borderwidth=2, relief="solid")
        self.battle_left_frame.grid(row=0, column=0, padx=20, pady=20)
        self.result_label = tk.Label(self.battle_left_frame, text="", bg="white", width=30, height=5, relief="sunken")
        self.result_label.pack(padx=10, pady=10)

        self.battle_right_frame = tk.Frame(self.battle_frame, borderwidth=2, relief="solid")
        self.battle_right_frame.grid(row=0, column=1, padx=20, pady=20)
        self.membership_label = tk.Label(self.battle_right_frame, text="Membership: ", bg="white", width=30, height=2)
        self.membership_label.pack(padx=10, pady=10)
        self.win_rate_label = tk.Label(self.battle_right_frame, text="Win Rate: ", bg="white", width=30, height=2)
        self.win_rate_label.pack(padx=10, pady=10)
        self.games_played_label = tk.Label(self.battle_right_frame, text="Games Played: ", bg="white", width=30, height=2)
        self.games_played_label.pack(padx=10, pady=10)
        self.script_label = tk.Label(self.battle_right_frame, text="Current Script: ", bg="white", width=30, height=2)
        self.script_label.pack(padx=10, pady=10)

        # Log Frame
        self.log_frame = tk.Frame(root, borderwidth=2, relief="solid")
        self.log_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(self.log_frame, text="Logs:", font=("Helvetica", 16)).pack(pady=5)
        self.log_text = tk.Text(self.log_frame, height=15, width=80)
        self.log_text.pack(padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check for admin credentials
        if username == "ADMIN" and password == "Root":
            self.current_player = Player(username, password, is_admin=1)
            self.log_event(f"Admin logged in: {username}")
            self.show_admin_panel()
            return

        # Check for player credentials
        cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', (username, password))
        player_data = cursor.fetchone()
        if player_data:
            self.current_player = Player(*player_data)
            self.log_event(f"Player logged in: {username}")
            self.update_battle_ui()
            self.show_battle_frame()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = simpledialog.askstring("Signup", "Enter new username:")
        password = simpledialog.askstring("Signup", "Enter new password:")
        if username and password:
            try:
                cursor.execute('INSERT INTO players (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                messagebox.showinfo("Signup Successful", "Account created successfully")
                self.log_event(f"New player signed up: {username}")
            except sqlite3.IntegrityError:
                messagebox.showerror("Signup Failed", "Username already exists")

    def show_battle_frame(self):
        self.login_frame.pack_forget()
        self.battle_frame.pack(padx=10, pady=10)

    def update_battle_ui(self):
        if self.current_player:
            self.membership_label.config(text=f"Membership: {self.current_player.membership}")
            self.win_rate_label.config(text=f"Win Rate: {self.current_player.win_rate}")
            self.games_played_label.config(text=f"Games Played: {self.current_player.games_played}")
            self.script_label.config(text=f"Current Script: {self.current_player.get_script()}")

    def start_6v6_battle(self):
        if self.current_player:
            result = f"6v6 battle result for {self.current_player.username}:\nVictory!"
            self.result_label.config(text=result)
            self.log_event(result)

    def start_3v3_battle(self):
        if self.current_player:
            result = f"3v3 battle result for {self.current_player.username}:\nDefeat!"
            self.result_label.config(text=result)
            self.log_event(result)

    def activate_script(self):
        if self.current_player and self.current_player.is_admin:
            activation_code = simpledialog.askstring("Activate Script", "Enter activation code:")
            if activation_code:
                if self.current_player.check_activation_code(activation_code):
                    messagebox.showinfo("Activation Success", "Script activated successfully")
                    self.current_player.is_script_activated = True
                    self.update_battle_ui()
                    self.log_event(f"Script activated for {self.current_player.username}")
                else:
                    messagebox.showerror("Activation Failed", "Invalid activation code")

    def show_admin_panel(self):
        if self.current_player and self.current_player.is_admin:
            admin_window = tk.Toplevel(self.root)
            admin_window.title("Admin Panel")

            tk.Button(admin_window, text="Generate Activation Code", command=self.generate_activation_code).pack(pady=10)
            tk.Button(admin_window, text="Promote User", command=self.promote_user).pack(pady=10)
            tk.Button(admin_window, text="Add New Script", command=self.add_new_script).pack(pady=10)

    def generate_activation_code(self):
        username = simpledialog.askstring("Generate Activation Code", "Enter username:")
        script_name = simpledialog.askstring("Generate Activation Code", "Enter script name:")
        if username and script_name:
            activation_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
            try:
                cursor.execute('INSERT INTO activation_codes (username, script_name, activation_code) VALUES (?, ?, ?)', (username, script_name, activation_code))
                conn.commit()
                messagebox.showinfo("Success", f"Activation code for {username} ({script_name}): {activation_code}")
                self.log_event(f"Activation code generated for {username} ({script_name}): {activation_code}")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Activation code for this script already exists for the user")

    def promote_user(self):
        username = simpledialog.askstring("Promote User", "Enter username to promote:")
        if username:
            cursor.execute('SELECT * FROM players WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                current_membership = user[2]
                new_membership = {"Junior": "Intermediate", "Intermediate": "Premium"}.get(current_membership)
                if new_membership:
                    cursor.execute('UPDATE players SET membership = ? WHERE username = ?', (new_membership, username))
                    conn.commit()
                    messagebox.showinfo("Success", f"{username} promoted to {new_membership}!")
                    self.log_event(f"User {username} promoted to {new_membership}")
                else:
                    messagebox.showinfo("No Promotion", f"{username} is already at the highest membership level")
            else:
                messagebox.showerror("Error", "User not found")

    def add_new_script(self):
        script_name = simpledialog.askstring("Add New Script", "Enter new script name:")
        script_description = simpledialog.askstring("Add New Script", "Enter script description:")
        if script_name and script_description:
            # Simulate adding a new script to the system
            scripts[script_name] = script_description
            messagebox.showinfo("Success", f"New script added: {script_name}")
            self.log_event(f"New script added: {script_name}")

    def show_tasks(self):
        tasks_window = tk.Toplevel(self.root)
        tasks_window.title("Tasks")
        tk.Label(tasks_window, text="Tasks for Players:", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(tasks_window, text="1. Complete 50 games to move from Junior to Intermediate membership.", padx=10, pady=10).pack()
        tk.Label(tasks_window, text="2. Complete 30 days of usage to maintain current membership status.", padx=10, pady=10).pack()

    def show_advertising(self):
        advertising_window = tk.Toplevel(self.root)
        advertising_window.title("Advertising")
        tk.Label(advertising_window, text="Advertising Information:", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(advertising_window, text="1. Check out our premium scripts for enhanced gameplay!", padx=10, pady=10).pack()
        tk.Label(advertising_window, text="2. Join our community for exclusive offers and updates.", padx=10, pady=10).pack()

    def log_event(self, event_description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"{timestamp} - {event_description}\n")
        self.log_text.yview(tk.END)

# Create the main window
root = tk.Tk()
app = BattleApp(root)
root.mainloop()

# Close the database connection
conn.close()
