import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import winsound
from player import Player
from player_database import PlayerDatabase
from udp_connection import UDPConnection
from countdown_timer import countdown_timer


class LaserTagMain:

    def __init__(self):

        self.db = PlayerDatabase()
        self.udp_connection = UDPConnection()

        self.root = tk.Tk()
        self.root.withdraw()

        # Splash audio
        self.load_splash_audio()
        self.show_splash_screen("logo.jpg")

        time.sleep(3)
        self.stop_audio()

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

    def load_splash_audio(self):
        try:
            winsound.PlaySound("splash.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            print("Error loading splash audio")

    def load_player_entry_audio(self):
        try:
            winsound.PlaySound("player_entry.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            print("Error loading player entry audio")

    def load_game_audio(self):
        try:
            winsound.PlaySound("game.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            print("Error loading game audio")

    def stop_audio(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    # ================= TIMER =================

    def update_timer(self):
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

        # Player entry audio
        self.load_player_entry_audio()

    def collect_players(self):

        players = []

        for rid, rcode in self.red_entries:

            pid = rid.get()
            code = rcode.get()

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
                    existing = self.db.get_codename(pid)
                    if existing is None:
                        self.db.add_player(pid,code)       

                player = Player(code, 1)
                players.append(player)

        for gid, gcode in self.green_entries:

            pid = gid.get()
            code = gcode.get()

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
                    existing = self.db.get_codename(pid)
                    if existing is None:
                        self.db.add_player(pid,code)

                player = Player(code, 2)
                players.append(player)

        return players

    def start_game(self):

        players = self.collect_players()

        if not players:
            messagebox.showerror("Error", "No players entered.")
            return

        if self.buildScreenClosed:
            messagebox.showerror("Error", "Game already running.")
            return

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
                print("Hardware ID for "+p.get_player_name()+f": {hid}")
                self.equipmentToPlayer[hid] = p
            try:
                self.udp_connection.send_to(p.get_player_num())
                response = self.udp_connection.recv_from()
            except Exception as e:
                print("UDP error:", e)

        self.root.withdraw()

        # Game audio
        self.stop_audio()
        self.load_game_audio()

        countdown_timer(
            self.root,
            30,
            lambda: self.show_play_action_screen(red_team, green_team)
        )

        self.gameStarted = True

    def start_game_f5(self):

        players = self.collect_players()

        if self.buildScreenClosed:
            messagebox.showerror("Error", "Game already running.")
            return

        red_team = []
        green_team = []

        for p in players:
            if p.team_code == 1:
                red_team.append(p)
            else:
                green_team.append(p)

        self.show_play_action_screen(red_team, green_team)
        self.gameStarted = True

    def show_play_action_screen(self, red_team, green_team):

        self.player_labels = {}

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Current Game Action")
        self.game_window.configure(bg="black")
        self.game_window.geometry("900x600")

        def on_close():
            self.game_window.destroy()
            self.root.deiconify()

        self.game_window.protocol("WM_DELETE_WINDOW", on_close)

        score_frame = tk.Frame(self.game_window, bg="black")
        score_frame.pack(pady=10)

        red_frame = tk.Frame(score_frame, bg="black")
        red_frame.pack(side="left", padx=80)

        tk.Label(red_frame, text="RED TEAM", fg="red", bg="black", font=("Arial", 16)).pack()
        self.red_score_label = tk.Label(red_frame, text="0", fg="red", bg="black", font=("Arial", 20))
        self.red_score_label.pack()

        for p in red_team:
            lbl = tk.Label(red_frame, text=f"{p.get_player_name()} - {p.get_score()}", fg="white", bg="black")
            lbl.pack()
            self.player_labels[p] = lbl

        green_frame = tk.Frame(score_frame, bg="black")
        green_frame.pack(side="right", padx=80)

        tk.Label(green_frame, text="GREEN TEAM", fg="lime", bg="black", font=("Arial", 16)).pack()
        self.green_score_label = tk.Label(green_frame, text="0", fg="lime", bg="black", font=("Arial", 20))
        self.green_score_label.pack()

        for p in green_team:
            lbl = tk.Label(green_frame, text=f"{p.get_player_name()} - {p.get_score()}", fg="white", bg="black")
            lbl.pack()
            self.player_labels[p] = lbl

        # TIMER UI
        self.time_remaining = 360

        self.timer_label = tk.Label(self.game_window,
                                   text="Time Remaining: 6:00",
                                   fg="white",
                                   bg="black",
                                   font=("Arial", 16))
        self.timer_label.pack(pady=10)

        self.update_timer()



    def edit_game(self):
        print("Edit Game")

    def parameters(self):
        print("Game Parameters")

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

    def view_game(self):
        print("View Game")

    def sync(self):
        print("Sync Equipment")

    def clear(self):
        for rid, rcode in self.red_entries:
            rid.delete(0, tk.END)
            rcode.delete(0, tk.END)

        for gid, gcode in self.green_entries:
            gid.delete(0, tk.END)
            gcode.delete(0, tk.END)

    def enter_hid(self, playerName):
        result = [None]
        dialog = tk.Toplevel()
        dialog.title("Input")
        dialog.configure(bg="black")
        dialog.geometry("300x150")
        dialog.grab_set()
        dialog.resizable(False, False)

        tk.Label(dialog, text="Enter the hardware ID for: "+playerName,
                 fg="cyan", bg="black").pack(pady=15)

        entry = tk.Entry(dialog)
        entry.pack()
        entry.focus_set()

        def submit():
            try:
                result[0] = int(entry.get())
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter a valid integer.", parent=dialog)

        entry.bind("<Return>", lambda e: submit())
        tk.Button(dialog, text="OK", command=submit).pack()

        dialog.wait_window()
        return result[0]

    def show_splash_screen(self, image_path):

        splash = tk.Toplevel(self.root)

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

        splash.after(3000, splash.destroy)


if __name__ == "__main__":
    LaserTagMain()
