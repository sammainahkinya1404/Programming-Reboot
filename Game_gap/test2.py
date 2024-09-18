import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
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
    is_admin INTEGER DEFAULT 0,
    is_activated INTEGER DEFAULT 0
)''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS activation_codes (
    username TEXT PRIMARY KEY,
    membership TEXT,
    activation_code TEXT
)''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_logs (
    username TEXT,
    log_event TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

# Scripts based on membership
scripts = {
    "Junior": "Basic Script",
    "Intermediate": "Advanced Script",
    "Premium": "Elite Script"
}

class Player:
    def __init__(self, username, password, membership="Junior", games_played=0, win_rate=0, days_used=0, is_admin=0, is_activated=0):
        self.username = username
        self.password = password
        self.membership = membership
        self.games_played = games_played
        self.win_rate = win_rate
        self.days_used = days_used
        self.script = scripts[membership]
        self.is_script_activated = False
        self.is_admin = is_admin
        self.is_activated = is_activated

    def upgrade_membership(self, new_membership):
        self.membership = new_membership
        self.script = scripts[new_membership]

    def check_activation_code(self, code):
        cursor.execute('SELECT activation_code FROM activation_codes WHERE username = ? AND membership = ?', (self.username, self.membership))
        result = cursor.fetchone()
        if result and result[0] == code:
            self.is_script_activated = True
            self.is_activated = 1
            cursor.execute('UPDATE players SET is_activated = 1 WHERE username = ?', (self.username,))
            conn.commit()
            return True
        return False

    def get_script(self):
        return self.script if self.is_script_activated else "Script not activated"

class BattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Simulation")
        self.current_player = None
        
        # Menu Bar
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
        
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2, pady=10)

        # Log Frame
        self.log_frame = tk.Frame(root, borderwidth=2, relief="solid")
        self.log_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(self.log_frame, text="Logs:", font=("Helvetica", 16)).pack(pady=5)
        self.log_text = tk.Text(self.log_frame, height=15, width=80)
        self.log_text.pack(padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "ADMIN" and password == "Root":
            self.current_player = Player(username, password, is_admin=1)
            self.log_event(f"Admin logged in: {username}")
            self.show_admin_panel()
            return

        cursor.execute('SELECT * FROM players WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()
        
        if result:
            self.current_player = Player(*result)
            self.update_player_stats()
            if not self.current_player.is_admin:
                if self.current_player.is_activated:
                    self.log_event(f"User logged in: {username}")
                else:
                    messagebox.showinfo("Activation Required", "Your account is not activated. Please activate it using the activation code.")
                    self.activate_script()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            try:
                cursor.execute('INSERT INTO players (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Account created successfully!")
                if not (username == "ADMIN"):
                    self.log_event(f"New account created: {username}")
                self.login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")

    def promote_player(self):
        username = simpledialog.askstring("Promote Player", "Enter the player's username:")
        new_membership = simpledialog.askstring("Promote Player", "Enter the new membership level (Junior/Intermediate/Premium):")
        if username and new_membership in scripts:
            cursor.execute('UPDATE players SET membership = ? WHERE username = ?', (new_membership, username))
            conn.commit()

            activation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            cursor.execute('INSERT OR REPLACE INTO activation_codes (username, membership, activation_code) VALUES (?, ?, ?)', (username, new_membership, activation_code))
            conn.commit()

            messagebox.showinfo("Success", f"{username} has been promoted to {new_membership} membership!\nActivation Code: {activation_code}")
            self.log_event(f"Player {username} promoted to {new_membership}. Activation code: {activation_code}")
        else:
            messagebox.showerror("Error", "Invalid input")

    def log_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not (self.current_player and self.current_player.is_admin):
            cursor.execute('INSERT INTO user_logs (username, log_event) VALUES (?, ?)', (self.current_player.username if self.current_player else 'Guest', event))
            conn.commit()

        self.log_text.insert(tk.END, f"[{timestamp}] {event}\n")
        self.log_text.see(tk.END)

    def activate_script(self):
        if self.current_player:
            code = simpledialog.askstring("Activation Code", "Enter the activation code:")
            
            if self.current_player.check_activation_code(code):
                messagebox.showinfo("Success", "Script activated successfully!")
                if not (self.current_player.is_admin):
                    self.log_event(f"Script activated for {self.current_player.username}")
                self.update_player_stats()
            else:
                messagebox.showerror("Error", "Invalid activation code")

    def update_player_stats(self):
        if self.current_player:
            stats = (
                f"Username: {self.current_player.username}\n"
                f"Membership: {self.current_player.membership}\n"
                f"Games Played: {self.current_player.games_played}\n"
                f"Win Rate: {self.current_player.win_rate:.2%}\n"
                f"Days Used: {self.current_player.days_used}\n"
                f"Script Status: {'Activated' if self.current_player.is_script_activated else 'Not Activated'}"
            )
            messagebox.showinfo("Player Stats", stats)

    def start_6v6_battle(self):
        result = self.simulate_battle(6, 6)
        self.log_event(f"6v6 Battle Result: {result}")

    def start_3v3_battle(self):
        result = self.simulate_battle(3, 3)
        self.log_event(f"3v3 Battle Result: {result}")

    def simulate_battle(self, team1_size, team2_size):
        if not self.current_player or not self.current_player.is_script_activated:
            return "Script not activated. Cannot start battle."
        # Simulate battle
        return "Team 1 wins!"  # Placeholder result

    def show_tasks(self):
        task_window = tk.Toplevel(self.root)
        task_window.title("Tasks")
        tk.Label(task_window, text="Here you can add tasks for players.", padx=20, pady=20).pack()

    def show_advertising(self):
        ad_window = tk.Toplevel(self.root)
        ad_window.title("Advertising")
        tk.Label(ad_window, text="Place your advertisements here.", padx=20, pady=20).pack()

    def show_admin_panel(self):
        if not (self.current_player and self.current_player.is_admin):
            messagebox.showerror("Error", "Access denied")
            return
        
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("400x300")

        tk.Label(admin_window, text="Admin Panel", font=('Helvetica', 16)).pack(pady=10)

        tk.Button(admin_window, text="Generate Code", command=self.generate_code).pack(pady=10)

        self.code_display = tk.Entry(admin_window, width=30)
        self.code_display.pack(pady=10)

        tk.Button(admin_window, text="Promote Player", command=self.promote_player).pack(pady=10)

    def generate_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.code_display.delete(0, tk.END)
        self.code_display.insert(0, code)

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleApp(root)
    root.mainloop()
