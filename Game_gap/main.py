import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Database setup
conn = sqlite3.connect('battle_game.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY, 
                    password TEXT, 
                    membership TEXT DEFAULT 'Junior', 
                    games_played INTEGER DEFAULT 0, 
                    win_rate REAL DEFAULT 0, 
                    days_used INTEGER DEFAULT 0)''')
conn.commit()

# Mock data for scripts
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

    def upgrade_membership(self):
        if self.games_played >= 50 and self.days_used >= 30 and self.membership == "Junior":
            self.membership = "Intermediate"
            self.script = scripts["Intermediate"]
        elif self.games_played >= 100 and self.days_used >= 15 and self.membership == "Intermediate":
            self.membership = "Premium"
            self.script = scripts["Premium"]

    def simulate_battle(self, mode):
        win_chance = 0.3 if self.membership == "Junior" else 0.6 if self.membership == "Intermediate" else 0.9
        battle_outcome = random.random() < win_chance
        if battle_outcome:
            self.win_rate += 1
        self.games_played += 1
        self.upgrade_membership()
        return battle_outcome

    def get_script(self):
        return self.script

class BattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Simulation")
        self.current_player = None

        # Main Layout
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

       # Horizontal Menu Bar
        self.menu_bar = tk.Frame(self.main_frame, bg="lightblue", padx=10, pady=5)
        self.menu_bar.pack(side="top", fill="x")

        # Navigation buttons
        self.login_button = tk.Button(self.menu_bar, text="Login/Signup", command=self.show_login_frame)
        self.login_button.pack(side="left", padx=5)

        self.tasks_button = tk.Button(self.menu_bar, text="Tasks", command=self.show_tasks)
        self.tasks_button.pack(side="left", padx=5)

        self.ads_button = tk.Button(self.menu_bar, text="Advertisements", command=self.show_ads)
        self.ads_button.pack(side="left", padx=5)

       

        # Battle and Stats area (right side)
        self.battle_frame = tk.Frame(self.main_frame, bg="white", padx=10, pady=10)
        self.battle_frame.pack(side="right", fill="both", expand=True)

        # Battle buttons
        self.battle_button_6v6 = tk.Button(self.battle_frame, text="Start 6v6 Wild Battle", command=self.start_6v6_battle)
        self.battle_button_6v6.pack(pady=10)

        self.battle_button_3v3 = tk.Button(self.battle_frame, text="Start 3v3 Competitive Battle", command=self.start_3v3_battle)
        self.battle_button_3v3.pack(pady=10)

        # Battle result label
        self.result_label = tk.Label(self.battle_frame, text="Battle Results", bg="white", width=30, height=5, relief="sunken")
        self.result_label.pack(pady=10)

        # Stats area
        self.stats_frame = tk.Frame(self.battle_frame, bg="white")
        self.stats_frame.pack(pady=10)

        self.membership_label = tk.Label(self.stats_frame, text="Membership: ", bg="white", width=30)
        self.membership_label.pack(pady=5)

        self.win_rate_label = tk.Label(self.stats_frame, text="Win Rate: ", bg="white", width=30)
        self.win_rate_label.pack(pady=5)

        self.games_played_label = tk.Label(self.stats_frame, text="Games Played: ", bg="white", width=30)
        self.games_played_label.pack(pady=5)

        self.script_label = tk.Label(self.stats_frame, text="Current Script: ", bg="white", width=30)
        self.script_label.pack(pady=5)
        
        
         # Bulletin Board
        self.bulletin_board_frame = tk.Frame(self.main_frame, bg="lightgray", height=100, relief="solid", bd=1)
        self.bulletin_board_frame.pack(side="top", fill="x")

        self.bulletin_board = tk.Label(self.bulletin_board_frame, text="Bulletin Board: Official Announcements", bg="lightgray", anchor="w", padx=10)
        self.bulletin_board.pack(fill="both", padx=10, pady=5)

    def show_login_frame(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login/Signup")

        tk.Label(login_window, text="Username").grid(row=0, column=0)
        username_entry = tk.Entry(login_window)
        username_entry.grid(row=0, column=1)

        tk.Label(login_window, text="Password").grid(row=1, column=0)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                self.current_player = Player(*user_data)
                login_window.destroy()
                self.update_labels()
            else:
                messagebox.showwarning("Login Failed", "Incorrect username or password.")

        tk.Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2)

    def show_tasks(self):
        messagebox.showinfo("Tasks", "No tasks available at the moment.")

    def show_ads(self):
        messagebox.showinfo("Advertisements", "No advertisements available at the moment.")

    def start_6v6_battle(self):
        if self.current_player:
            result = self.current_player.simulate_battle("6v6 Wild")
            self.result_label.config(text="6v6 Wild Battle Result: " + ("You won!" if result else "You lost!"))
            self.update_labels()
            self.save_player_data()

    def start_3v3_battle(self):
        if self.current_player:
            result = self.current_player.simulate_battle("3v3 Competitive")
            self.result_label.config(text="3v3 Competitive Battle Result: " + ("You won!" if result else "You lost!"))
            self.update_labels()
            self.save_player_data()

    def update_labels(self):
        if self.current_player:
            self.membership_label.config(text=f"Membership: {self.current_player.membership}")
            self.win_rate_label.config(text=f"Win Rate: {self.current_player.win_rate}")
            self.games_played_label.config(text=f"Games Played: {self.current_player.games_played}")
            self.script_label.config(text=f"Current Script: {self.current_player.get_script()}")

    def save_player_data(self):
        cursor.execute("UPDATE users SET membership = ?, games_played = ?, win_rate = ?, days_used = ? WHERE username = ?",
                       (self.current_player.membership, self.current_player.games_played, self.current_player.win_rate, self.current_player.days_used, self.current_player.username))
        conn.commit()

# Run the Tkinter App
root = tk.Tk()
app = BattleApp(root)
root.mainloop()
