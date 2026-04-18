import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import pygame
from player import Player
from player_database import PlayerDatabase
from udp_connection import UDPConnection
from countdown_timer import countdown_timer


class LaserTagMain:

    def __init__(self):

        # Init audio (cross-platform)
        pygame.mixer.init()

        self.db = PlayerDatabase()
        self.udp_connection = UDPConnection()

        self.root = tk.Tk()
        self.root.withdraw()

        # Splash audio
        self.load_splash_audio()
        self.show_splash_screen("logo.jpg")

        # Replace sleep with after
        self.root.after(3000, self.stop_audio)

        self.root.deiconify()
        self.root.title("Edit Current Game")
        self.root.configure(bg="black")
        self.root.geometry("1000x700")

        self.buildScreen = False
        self.buildScreenClosed = False
        self.gameStarted = False

        self.build_interface()

        self.root.bind("<F1>", lambda e: self.edit_game())
        self.root.bind("<F2>", lambda e: self.parameters())
        self.root.bind("<F3>", lambda e: self.start_game())
        self.root.bind("<F5>", lambda e: self.display_switch())
        self.root.bind("<F8>", lambda e: self.view_game())
        self.root.bind("<F10>", lambda e: self.sync())
        self.root.bind("<F12>", lambda e: self.clear())

        self.root.mainloop()

    # ================= AUDIO =================

    def play_audio(self, file):
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
        except:
            print(f"Error loading audio: {file}")

    def load_splash_audio(self):
        self.play_audio("splash.wav")

    def load_player_entry_audio(self):
        self.play_audio("player_entry.wav")

    def load_game_audio(self):
        self.play_audio("game.wav")

    def stop_audio(self):
        pygame.mixer.music.stop()

    # ================= TIMER =================

    def update_timer(self):

        if not hasattr(self, "game_window") or not self.game_window.winfo_exists():
            return

        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60

        self.timer_label.config(
            text=f"Time Remaining: {minutes}:{seconds:02d}"
        )

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.game_window.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Game Over", "Time has expired!")
            self.stop_audio()

    # ================= UI =================

    def build_interface(self):

        self.build_frame = tk.Frame(self.root, bg="black")
        self.build_frame.place(relwidth=1, relheight=1)

        title = tk.Label(self.build_frame, text="Edit Current Game",
                         fg="cyan", bg="black",
                         font=("Arial", 20))
        title.pack(pady=10)

        main_frame = tk.Frame(self.build_frame, bg="black")
        main_frame.pack()

        red_frame = tk.Frame(main_frame, bg="#330000")
        red_frame.grid(row=0, column=0, padx=40)

        tk.Label(red_frame, text="RED TEAM",
                 fg="white", bg="#550000",
                 font=("Arial", 14)).grid(row=0, column=0, columnspan=3, sticky="ew")

        green_frame = tk.Frame(main_frame, bg="#003300")
        green_frame.grid(row=0, column=1, padx=40)

        tk.Label(green_frame, text="GREEN TEAM",
                 fg="white", bg="#005500",
                 font=("Arial", 14)).grid(row=0, column=0, columnspan=3, sticky="ew")

        self.red_entries = []
        self.green_entries = []

        for i in range(20):

            tk.Label(red_frame, text=i+1, fg="white", bg="#330000").grid(row=i+1, column=0)

            rid = tk.Entry(red_frame, width=10)
            rcode = tk.Entry(red_frame, width=12)

            rid.grid(row=i+1, column=1)
            rcode.grid(row=i+1, column=2)

            self.red_entries.append((rid, rcode))

            tk.Label(green_frame, text=i+1, fg="white", bg="#003300").grid(row=i+1, column=0)

            gid = tk.Entry(green_frame, width=10)
            gcode = tk.Entry(green_frame, width=12)

            gid.grid(row=i+1, column=1)
            gcode.grid(row=i+1, column=2)

            self.green_entries.append((gid, gcode))

        bottom = tk.Frame(self.build_frame, bg="black")
        bottom.pack(pady=20)

        buttons = [
            ("F1 Edit Game", self.edit_game),
            ("F2 Game Parameters", self.parameters),
            ("F3 Start Game", self.start_game),
            ("F5 Switch Display", self.display_switch),
            ("F8 View Game", self.view_game),
            ("F10 Flick Sync", self.sync),
            ("F12 Clear Game", self.clear)
        ]

        for text, cmd in buttons:
            b = tk.Button(bottom, text=text, width=16, command=cmd)
            b.pack(side="left", padx=5)

        self.buildScreen = True
        self.build_frame.tkraise()

        self.load_player_entry_audio()

    # ================= PLAYER COLLECTION =================

    def collect_players(self):

        players = []

        for entries, team in [(self.red_entries, 1), (self.green_entries, 2)]:
            for pid_entry, code_entry in entries:

                pid = pid_entry.get()
                code = code_entry.get()

                if pid:

                    try:
                        pid = int(pid)
                    except ValueError:
                        messagebox.showerror("Error", "Player ID must be a number")
                        return []

                    if not code:
                        code = self.db.get_codename(pid)
                        if code is None:
                            code = "Player" + str(pid)
                            self.db.add_player(pid, code)
                    else:
                        if self.db.get_codename(pid) is None:
                            self.db.add_player(pid, code)

                    players.append(Player(code, team))

        return players

    # ================= GAME START =================

    def start_game(self):

        players = self.collect_players()

        if not players:
            messagebox.showerror("Error", "No players entered.")
            return

        if self.buildScreenClosed:
            messagebox.showerror("Error", "Game already running.")
            return

        self.buildScreenClosed = True

        red_team = [p for p in players if p.team_code == 1]
        green_team = [p for p in players if p.team_code == 2]

        self.root.withdraw()

        self.stop_audio()
        self.load_game_audio()

        countdown_timer(
            self.root,
            30,
            lambda: self.show_play_action_screen(red_team, green_team)
        )

    def start_game_f5(self):

        players = self.collect_players()

        if not players:
            messagebox.showerror("Error", "No players entered.")
            return

        if self.buildScreenClosed:
            messagebox.showerror("Error", "Game already running.")
            return

        red_team = [p for p in players if p.team_code == 1]
        green_team = [p for p in players if p.team_code == 2]

        self.show_play_action_screen(red_team, green_team)

    # ================= GAME WINDOW =================

    def show_play_action_screen(self, red_team, green_team):

        self.player_labels = {}

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Current Game Action")
        self.game_window.configure(bg="black")
        self.game_window.geometry("900x600")

        def on_close():
            self.stop_audio()
            self.game_window.destroy()
            self.root.deiconify()
            self.buildScreenClosed = False

        self.game_window.protocol("WM_DELETE_WINDOW", on_close)

        score_frame = tk.Frame(self.game_window, bg="black")
        score_frame.pack(pady=10)

        # RED
        red_frame = tk.Frame(score_frame, bg="black")
        red_frame.pack(side="left", padx=80)

        tk.Label(red_frame, text="RED TEAM", fg="red", bg="black").pack()
        self.red_score_label = tk.Label(red_frame, text="0", fg="red", bg="black")
        self.red_score_label.pack()

        for p in red_team:
            lbl = tk.Label(red_frame, text=f"{p.get_player_name()} - 0", fg="white", bg="black")
            lbl.pack()
            self.player_labels[id(p)] = lbl

        # GREEN
        green_frame = tk.Frame(score_frame, bg="black")
        green_frame.pack(side="right", padx=80)

        tk.Label(green_frame, text="GREEN TEAM", fg="lime", bg="black").pack()
        self.green_score_label = tk.Label(green_frame, text="0", fg="lime", bg="black")
        self.green_score_label.pack()

        for p in green_team:
            lbl = tk.Label(green_frame, text=f"{p.get_player_name()} - 0", fg="white", bg="black")
            lbl.pack()
            self.player_labels[id(p)] = lbl

        # TIMER
        self.time_remaining = 360

        self.timer_label = tk.Label(self.game_window,
                                   text="Time Remaining: 6:00",
                                   fg="white", bg="black")
        self.timer_label.pack(pady=10)

        self.update_timer()

    # ================= SCORE =================

    def update_scores(self, player, points):

        player.add_score(points)

        if player.team_code == 1:
            current = int(self.red_score_label["text"])
            self.red_score_label.config(text=str(current + points))
        else:
            current = int(self.green_score_label["text"])
            self.green_score_label.config(text=str(current + points))

        self.player_labels[id(player)].config(
            text=f"{player.get_player_name()} - {player.get_score()}"
        )

    # ================= OTHER =================

    def edit_game(self): print("Edit Game")
    def parameters(self): print("Game Parameters")
    def view_game(self): print("View Game")
    def sync(self): print("Sync Equipment")

    def display_switch(self):
        if self.buildScreen:
            self.root.withdraw()
            self.start_game_f5()
            self.buildScreen = False
        else:
            if hasattr(self, 'game_window') and self.game_window.winfo_exists():
                self.game_window.withdraw()
            self.root.deiconify()
            self.build_frame.tkraise()
            self.buildScreen = True

    def clear(self):
        for entries in [self.red_entries, self.green_entries]:
            for a, b in entries:
                a.delete(0, tk.END)
                b.delete(0, tk.END)

    # ================= SPLASH =================

    def show_splash_screen(self, image_path):

        splash = tk.Toplevel(self.root)

        try:
            image = Image.open(image_path)
        except:
            splash.destroy()
            return

        image = image.resize((800, 600), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(splash, image=photo)
        label.image = photo
        label.pack()

        splash.after(3000, splash.destroy)


if __name__ == "__main__":
    LaserTagMain()
