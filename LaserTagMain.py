# laser_tag_main.py
# Full version with cross-platform audio + non-blocking splash timing + minimal fixes

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import ipaddress
import pygame
from player import Player
from player_database import PlayerDatabase
from udp_connection import UDPConnection
from countdown_timer import countdown_timer
from friendly_fire import handle_hit


# ==========================================================
# AUDIO MANAGER (cross-platform)
# ==========================================================
class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.ready = True
        except Exception as e:
            print("Audio init failed:", e)
            self.ready = False

    def play_music(self, filename):
        if not self.ready:
            return
        if not os.path.exists(filename):
            print("Missing audio:", filename)
            return
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        except Exception as e:
            print("Music play failed:", e)

    def play_sound(self, filename):
        if not self.ready:
            return
        if not os.path.exists(filename):
            print("Missing audio:", filename)
            return
        try:
            sound = pygame.mixer.Sound(filename)
            sound.play()
        except Exception as e:
            print("Sound play failed:", e)


# ==========================================================
# MAIN APP
# ==========================================================
class LaserTagMain:

    def __init__(self):

        self.db = PlayerDatabase()
        self.udp_connection = UDPConnection()
        self.audio = AudioManager()

        self.root = tk.Tk()
        self.root.withdraw()

        self.show_splash_screen("logo.jpg")

        # non-blocking startup after splash
        self.root.after(3000, self.finish_startup)
        self.root.mainloop()

    # ======================================================
    # STARTUP
    # ======================================================
    def finish_startup(self):

        self.root.deiconify()
        self.root.title("Edit Current Game")
        self.root.configure(bg="black")
        self.root.geometry("1000x700")

        self.buildScreen = False
        self.buildScreenClosed = False
        self.gameStarted = False
        self.flash_state = False

        self.build_interface()

        self.root.bind("<F1>", lambda e: self.edit_game())
        self.root.bind("<F2>", lambda e: self.edit_ip_address())
        self.root.bind("<F3>", lambda e: self.start_game())
        self.root.bind("<F5>", lambda e: self.display_switch())
        self.root.bind("<F8>", lambda e: self.view_game())
        self.root.bind("<F10>", lambda e: self.sync())
        self.root.bind("<F12>", lambda e: self.clear())

    # ======================================================
    # UI BUILD
    # ======================================================
    def build_interface(self):

        self.build_frame = tk.Frame(self.root, bg="black")
        self.build_frame.place(relwidth=1, relheight=1)

        title = tk.Label(
            self.build_frame,
            text="Edit Current Game",
            fg="cyan",
            bg="black",
            font=("Arial", 20)
        )
        title.pack(pady=10)

        main_frame = tk.Frame(self.build_frame, bg="black")
        main_frame.pack()

        red_frame = tk.Frame(main_frame, bg="#330000")
        red_frame.grid(row=0, column=0, padx=40)

        tk.Label(
            red_frame,
            text="RED TEAM",
            fg="white",
            bg="#550000",
            font=("Arial", 14)
        ).grid(row=0, column=0, columnspan=3, sticky="ew")

        green_frame = tk.Frame(main_frame, bg="#003300")
        green_frame.grid(row=0, column=1, padx=40)

        tk.Label(
            green_frame,
            text="GREEN TEAM",
            fg="white",
            bg="#005500",
            font=("Arial", 14)
        ).grid(row=0, column=0, columnspan=3, sticky="ew")

        self.red_entries = []
        self.green_entries = []

        for i in range(20):

            # red
            tk.Label(
                red_frame,
                text=i + 1,
                fg="white",
                bg="#330000"
            ).grid(row=i + 1, column=0)

            rid = tk.Entry(red_frame, width=10)
            rcode = tk.Entry(red_frame, width=12)

            rid.grid(row=i + 1, column=1)
            rcode.grid(row=i + 1, column=2)

            self.red_entries.append((rid, rcode))

            # green
            tk.Label(
                green_frame,
                text=i + 1,
                fg="white",
                bg="#003300"
            ).grid(row=i + 1, column=0)

            gid = tk.Entry(green_frame, width=10)
            gcode = tk.Entry(green_frame, width=12)

            gid.grid(row=i + 1, column=1)
            gcode.grid(row=i + 1, column=2)

            self.green_entries.append((gid, gcode))

        bottom = tk.Frame(self.build_frame, bg="black")
        bottom.pack(pady=20)

        buttons = [
            ("F1 Edit Game", self.edit_game),
            ("F2 Parameters", self.edit_ip_address),
            ("F3 Start Game", self.start_game),
            ("F5 Switch Display", self.display_switch),
            ("F8 View Game", self.view_game),
            ("F10 Sync", self.sync),
            ("F12 Clear", self.clear)
        ]

        for text, cmd in buttons:
            tk.Button(
                bottom,
                text=text,
                width=16,
                command=cmd
            ).pack(side="left", padx=5)

        self.buildScreen = True

    # ======================================================
    # PLAYER COLLECTION
    # ======================================================
    def collect_players(self):

        players = []

        # RED TEAM
        for rid, rcode in self.red_entries:

            pid = rid.get().strip()
            code = rcode.get().strip()

            if pid:

                try:
                    pid = int(pid)
                except ValueError:
                    messagebox.showerror("Error", "Player ID must be numeric")
                    return []

                if not code:
                    code = self.db.get_codename(pid)

                    if code is None:
                        code = "Player" + str(pid)
                        self.db.add_player(pid, code)
                else:
                    #saving entered codename to database if it doesn't exit already
                    existing = self.db.get_codename(pid)
                    if existing is None:
                        self.db.add_player(pid,code) 

                players.append(Player(code, 1))

        # GREEN TEAM
        for gid, gcode in self.green_entries:

            pid = gid.get().strip()
            code = gcode.get().strip()

            if pid:

                try:
                    pid = int(pid)
                except ValueError:
                    messagebox.showerror("Error", "Player ID must be numeric")
                    return []

                if not code:
                    code = self.db.get_codename(pid)

                    if code is None:
                        code = "Player" + str(pid)
                        self.db.add_player(pid, code)
                else:
                    #saving entered codename to database if it doesn't exit already
                    existing = self.db.get_codename(pid)
                    if existing is None:
                        self.db.add_player(pid,code) 

                players.append(Player(code, 2))

        return players

    # ======================================================
    # GAME START
    # ======================================================
    def start_game(self):

        players = self.collect_players()

        if not players:
            messagebox.showerror("Error", "No players entered.")
            return

        if self.buildScreenClosed:
            messagebox.showerror("Error", "Game already running.")
            return

        self.audio.play_music("start.mp3")

        red_team = []
        green_team = []

        for p in players:
            if p.team_code == 1:
                red_team.append(p)
            else:
                green_team.append(p)

        self.equipmentToPlayer = {}
        self.base_hit = set()

        for p in players:

            hid = self.enter_hid(p.get_player_name())

            if hid is not None:
                self.equipmentToPlayer[hid] = p

            try:
                self.udp_connection.send_to(p.get_player_num())
                self.udp_connection.recv_from()
            except Exception as e:
                print("UDP error:", e)

        self.root.withdraw()

        countdown_timer(
            self.root,
            30,
            lambda: self.show_play_action_screen(red_team, green_team)
        )

        self.gameStarted = True

    # ======================================================
    # BASE SCORING
    # ======================================================
    def baseScoring(self, equipment_id, base_color):

        if equipment_id in self.base_hit:
            return

        if equipment_id not in self.equipmentToPlayer:
            return

        player = self.equipmentToPlayer[equipment_id]

        if base_color == "green" and player.team_code == 2:
            return

        if base_color == "red" and player.team_code == 1:
            return

        player.add_score(100)
        self.base_hit.add(equipment_id)

        self.audio.play_sound("score.wav")

        self.update_playerDisplay(player)

    # ======================================================
    # SCOREBOARD
    # ======================================================
    def updateTeamScores(self):

        red_total = 0
        green_total = 0

        for player in self.player_labels:

            if player.team_code == 1:
                red_total += player.get_score()
            else:
                green_total += player.get_score()

        self.red_score_label.config(text=str(red_total))
        self.green_score_label.config(text=str(green_total))

    def update_playerDisplay(self, player):

        if player in self.player_labels:

            label = self.player_labels[player]

            try:
                icon = Image.open("baseicon.jpg")
                icon = icon.resize((20, 20), Image.LANCZOS)
                photo = ImageTk.PhotoImage(icon)

                label.config(
                    text=f"{player.get_player_name()} - {player.get_score()}",
                    image=photo,
                    compound="left"
                )

                label.image = photo

            except Exception:
                pass

        self.updateTeamScores()

    def start_scoreFlashing(self):
        self.flash_timer()

    def flash_timer(self):
        if self.flash_state is None:
            return 
        
        red_total = 0
        green_total = 0

        for player in self.player_labels:
            if player.team_code == 1:
                red_total += player.get_score()
            else:
                green_total += player.get_score()

        #winner will be flashing
        if red_total > green_total:
            color = "red" if self.flash_state else "darkred"
            self.red_score_label.config(fg=color)
        elif green_total > red_total:
            color = "lime" if self.flash_state else "darkgreen"
            self.green_score_label.config(fg=color)
        
        #toggling state
        self.flash_state = not self.flash_state

        self.root.after(500, self.flash_timer)



    # ======================================================
    # GAME SCREEN
    # ======================================================
    def show_play_action_screen(self, red_team, green_team):

        self.player_labels = {}

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Current Game Action")
        self.game_window.configure(bg="black")
        self.game_window.geometry("900x600")

        def on_close():
            self.flash_state = None
            self.game_window.destroy()
            self.root.deiconify()

        self.game_window.protocol("WM_DELETE_WINDOW", on_close)

        score_frame = tk.Frame(self.game_window, bg="black")
        score_frame.pack(pady=10)

        red_frame = tk.Frame(score_frame, bg="black")
        red_frame.pack(side="left", padx=80)

        tk.Label(
            red_frame,
            text="RED TEAM",
            fg="red",
            bg="black",
            font=("Arial", 16)
        ).pack()

        self.red_score_label = tk.Label(
            red_frame,
            text="0",
            fg="red",
            bg="black",
            font=("Arial", 20)
        )
        self.red_score_label.pack()

        for p in red_team:
            lbl = tk.Label(
                red_frame,
                text=f"{p.get_player_name()} - {p.get_score()}",
                fg="white",
                bg="black"
            )
            lbl.pack()
            self.player_labels[p] = lbl

        green_frame = tk.Frame(score_frame, bg="black")
        green_frame.pack(side="right", padx=80)

        tk.Label(
            green_frame,
            text="GREEN TEAM",
            fg="lime",
            bg="black",
            font=("Arial", 16)
        ).pack()

        self.green_score_label = tk.Label(
            green_frame,
            text="0",
            fg="lime",
            bg="black",
            font=("Arial", 20)
        )
        self.green_score_label.pack()

        for p in green_team:
            lbl = tk.Label(
                green_frame,
                text=f"{p.get_player_name()} - {p.get_score()}",
                fg="white",
                bg="black"
            )
            lbl.pack()
            self.player_labels[p] = lbl

        #readding box and static timer
        action_frame = tk.Frame(self.game_window, bg ="black")
        action_frame.pack(pady=20)

        tk.Label(
            action_frame, 
            text="Current Game Action", 
            fg="white", 
            bg="black", 
            font=("Arial", 14)
        ).pack()

        self.action_log = tk.Text(
            action_frame, 
            width=70, 
            height=15, 
            bg="navy", 
            fg="white"
        )
        self.action_log.pack()

        # TIMER
        self.timer_label = tk.Label(
            self.game_window, 
            text="Time Remaining: 6:00", 
            fg="white", 
            bg="black", 
            font=("Arial", 16)
        )
        self.timer_label.pack(pady=10)

        self.buildScreen = False
        self.run_traffic()

        self.start_scoreFlashing()

    # ======================================================
    # MISC
    # ======================================================
    def edit_game(self):
        print("Edit Game")

    def parameters(self):
        print("Game Parameters")

    def display_switch(self):

        if self.buildScreen:
            self.root.withdraw()
        else:
            self.root.deiconify()
            self.build_frame.tkraise()

        self.buildScreen = not self.buildScreen

    def view_game(self):
        print("View Game")

    def sync(self):
        print("Sync")

    def clear(self):

        for rid, rcode in self.red_entries:
            rid.delete(0, tk.END)
            rcode.delete(0, tk.END)

        for gid, gcode in self.green_entries:
            gid.delete(0, tk.END)
            gcode.delete(0, tk.END)

    # ======================================================
    # HID ENTRY
    # ======================================================
    def edit_ip_address(self):
        result = [None]  
        dialog = tk.Toplevel()
        dialog.title("Input")
        dialog.configure(bg="black")
        dialog.geometry("300x150")
        dialog.grab_set()  
        dialog.resizable(False, False)
        
        dialog.update_idletasks()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 150
        y = (screen_h // 2) - 75
        dialog.geometry(f"+{x}+{y}")
    
        tk.Label(dialog, text="Enter the new IP address: ", fg="cyan", bg="black",
                 font=("Arial", 15)).pack(pady=15)
    
        entry = tk.Entry(dialog, width=20, font=("Arial", 15),
                         justify="center")
        entry.pack()
        entry.focus_set()  # Auto-focus the entry box
    
        def submit():
            user_input = entry.get().strip() # Get input and remove whitespace
            try:
                # This will validate if the string is a proper IPv4 or IPv6 address
                ipaddress.ip_address(user_input)
                
                # If valid, store the string in result[0] and close the dialog
                result[0] = user_input
                dialog.destroy()
            except ValueError:
                # If the input isn't a valid IP, show an error and clear the entry box
                messagebox.showerror("Invalid Input", "Please enter a valid IP address (e.g., 127.0.0.1).", parent=dialog)
                entry.delete(0, tk.END)
        return result[0]
    
    def enter_hid(self, playerName):

        result = [None]

        dialog = tk.Toplevel()
        dialog.title("Input")
        dialog.configure(bg="black")
        dialog.geometry("300x150")
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Enter hardware ID for: " + playerName,
            fg="cyan",
            bg="black"
        ).pack(pady=15)

        entry = tk.Entry(dialog, width=20)
        entry.pack()
        entry.focus_set()

        def submit():
            try:
                result[0] = int(entry.get())
                dialog.destroy()
            except ValueError:
                messagebox.showerror(
                    "Invalid",
                    "Enter a valid number",
                    parent=dialog
                )

        entry.bind("<Return>", lambda e: submit())

        tk.Button(
            dialog,
            text="OK",
            command=submit
        ).pack(pady=10)

        dialog.wait_window()

        return result[0]
    # ======================================================
    # SPLASH
    # ======================================================
    def show_splash_screen(self, image_path):

        splash = tk.Toplevel(self.root)
        splash.title("Splash")

        try:
            image = Image.open(image_path)
        except Exception:
            splash.destroy()
            return

        image = image.resize((800, 600), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(splash, image=photo)
        label.image = photo
        label.pack()

        splash.geometry("800x600")

        x = (splash.winfo_screenwidth() // 2) - 400
        y = (splash.winfo_screenheight() // 2) - 300

        splash.geometry(f"+{x}+{y}")

        self.audio.play_music("intro.mp3")

        splash.after(3000, splash.destroy)
    
    # Friendly fire helper methods
    def process_hit_message(self, message):
        try:
            if ":" not in message:
                return

            shooter_id_str, target_id_str = message.split(":")
            shooter_id = int(shooter_id_str)
            target_id = int(target_id_str)

            shooter = self.equipmentToPlayer.get(shooter_id)
            target = self.equipmentToPlayer.get(target_id)

            result = handle_hit(shooter, target)
            self.refresh_player_scores()

            if shooter is not None and target is not None and shooter.team_code == target.team_code:
                self.udp_connection.send_to(shooter_id)
                self.udp_connection.send_to(target_id)
            else:
                if target is not None:
                    self.udp_connection.send_to(target_id)

        except Exception as e:
            print("Hit processing error:", e)

    # Friendly fire helper method
    def refresh_player_scores(self):
        for player, label in self.player_labels.items():
            current_image = getattr(label, "image", "")
            if current_image:
                label.config(
                    text=f"{player.get_player_name()} - {player.get_score()}",
                    image=current_image,
                    compound="left"
                )
            else:
                label.config(text=f"{player.get_player_name()} - {player.get_score()}")

        self.updateTeamScores()

    # Friendly fire helper method
    def poll_udp(self):
        try:
            data = self.udp_connection.recv_from()

            if data is not None:
                self.process_hit_message(data)

        except Exception as e:
            print("UDP poll error:", e)

        if hasattr(self, 'game_window') and self.game_window.winfo_exists():
            self.game_window.after(50, self.poll_udp)

    def run_traffic(self):
        if hasattr(self, 'game_window') and self.game_window.winfo_exists():
            code = (self.udp_connection.recv_from())
            if code:
                try:
                    #self.codes = code.split(":")
                    self.int_code1 = int(code[0:1])
                    self.int_code2 = int(code[2:4]) 
                    self.udp_connection.send_to("404")
                    if self.int_code2 == 43:
                        self.baseScoring(self.int_code1, 'green')
                    elif self.int_code2 == 53:
                        self.baseScoring(self.int_code1, 'red')
                    elif self.int_code1 % 2 == self.int_code2 % 2: # They are on the same team
                        self.udp_connection.send_to("504")
                        player1 = self.equipmentToPlayer[self.int_code1]
                        player2 = self.equipmentToPlayer[self.int_code2]
                        print(f"Player {player1.get_player_name()} hit player {player2.get_player_name()}!")
                        player1.add_score(-10)
                        player2.add_score(-10)
                    else:
                        player1 = self.equipmentToPlayer[self.int_code1]
                        player2 = self.equipmentToPlayer[self.int_code2]
                        print(f"Player {player1.get_player_name()} hit player {player2.get_player_name()}!")
                        player1.add_score(10)
                except ValueError:
                    print("Error in parsing int from received code")

                self.game_window.after(50, self.run_traffic)
    


# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    LaserTagMain()
