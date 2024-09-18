import tkinter as tk
from tkinter import messagebox
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
    days_used INTEGER DEFAULT 0
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS activation_codes (
    script_name TEXT PRIMARY KEY,
    activation_code TEXT
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
    def __init__(self, username, password, membership="Junior", games_played=0, win_rate=0, days_used=0):
        self.username = username
        self.password = password
        self.membership = membership
        self.games_played = games_played
        self.win_rate = win_rate
        self.days_used = days_used
        self.script = scripts[membership]
        self.is_script_activated = False  # Track if the script is activated

    def upgrade_membership(self):
        if self.games_played >= 50 and self.days_used >= 30 and self.membership == "Junior":
            self.membership = "Intermediate"
            self.script = scripts["Intermediate"]
        elif self.games_played >= 100 and self.days_used >= 15 and self.membership == "Intermediate":
            self.membership = "Premium"
            self.script = scripts["Premium"]

    def check_activation_code(self, code):
        cursor.execute('SELECT activation_code FROM activation_codes WHERE script_name = ?', (self.script,))
        result = cursor.fetchone()
        if result and result[0] == code:
            self.is_script_activated = True
            return True
        return False

    def get_script(self):
        return self.script if self.is_script_activated else "Script not activated"

    def log_action(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {self.username}: {action}"
        return log_entry

class BattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Simulation")
        self.current_player = None

        # Menu Bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        menu_options = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_options)
        menu_options.add_command(label="Log In", command=self.login)
        menu_options.add_command(label="Signup", command=self.signup)
        menu_options.add_separator()
        menu_options.add_command(label="To Do Battle", command=self.start_6v6_battle)
        menu_options.add_command(label="Advertising")
        menu_options.add_command(label="Activate Script", command=self.activate_script)

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

        tk.Button(self.battle_left_frame, text="Start 6v6 Wild Battle", command=self.start_6v6_battle).pack(padx=10, pady=10)
        tk.Button(self.battle_left_frame, text="Start 3v3 Competitive Battle", command=self.start_3v3_battle).pack(padx=10, pady=10)

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
        if username and password:
            self.current_player = Player(username, password)
            self.update_player_stats()
            self.log_event(f"Player logged in: {username}")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            cursor.execute('INSERT INTO players (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.log_event(f"New account created: {username}")
            self.login()

    def update_player_stats(self):
        if self.current_player:
            self.membership_label.config(text=f"Membership: {self.current_player.membership}")
            self.win_rate_label.config(text=f"Win Rate: {self.current_player.win_rate:.2%}")
            self.games_played_label.config(text=f"Games Played: {self.current_player.games_played}")
            self.script_label.config(text=f"Current Script: {self.current_player.get_script()}")

    def start_6v6_battle(self):
        result = self.simulate_battle(6, 6)
        self.result_label.config(text=result)
        self.log_event(f"6v6 Battle Result: {result}")

    def start_3v3_battle(self):
        result = self.simulate_battle(3, 3)
        self.result_label.config(text=result)
        self.log_event(f"3v3 Battle Result: {result}")

    def simulate_battle(self, team1_size, team2_size):
        if self.current_player:
            outcome = random.choice(["Victory", "Defeat"])
            self.current_player.games_played += 1
            if outcome == "Victory":
                self.current_player.win_rate = ((self.current_player.win_rate * (self.current_player.games_played - 1)) + 1) / self.current_player.games_played
            else:
                self.current_player.win_rate = (self.current_player.win_rate * (self.current_player.games_played - 1)) / self.current_player.games_played
            self.current_player.upgrade_membership()
            self.update_player_stats()
            return f"Team 1 ({team1_size}) vs Team 2 ({team2_size}): {outcome}"
        return "Login required to start battle"

    def activate_script(self):
        if self.current_player:
            code = tk.simpledialog.askstring("Activation Code", "Enter your activation code:")
            if code and self.current_player.check_activation_code(code):
                messagebox.showinfo("Success", "Script activated successfully!")
                self.log_event("Script activated")
            else:
                messagebox.showerror("Error", "Invalid activation code!")
                self.log_event("Failed to activate script")

    def log_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {event}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)  # Scroll to the latest log

root = tk.Tk()
app = BattleApp(root)
root.mainloop()
