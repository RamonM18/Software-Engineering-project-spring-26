import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import winsound
from player import Player
from player_database import PlayerDatabase
from udp_connection import UDPConnection
from countdown_timer import countdown_timer
import ipaddress

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
        self.root.bind("<F2>", lambda e: self.edit_ip_address())
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
            #("F1 Edit Game", self.edit_game),
            ("F2 Change IP address", self.edit_ip_address),
            ("F3 Start Game", self.start_game),
            ("F5 Switch Display", self.display_switch),
            #("F8 View Game", self.view_game),
            #("F10 Flick Sync", self.sync),
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
                self.udp_connection.send_to(str(hid)) #I'm not totally sure about putting this here, doesn't really serve any purpose but is in the project description
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
        
        self.udp_connection.send_to("202")
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
        self.udp_connection.send_to(202)
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


        self.buildScreen = False
        self.run_traffic()

    def edit_game(self):
        print("Edit Game")

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
    
        def on_enter(event):
            submit()
    
        entry.bind("<Return>", on_enter)  # Allow Enter key to submit
        tk.Button(dialog, text="OK", width=10, command=submit).pack(pady=10)
    
        dialog.wait_window()  # Wait until dialog closes before returning
        self.udp_connection.set_network_address(result[0])

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
        
        dialog.update_idletasks()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 150
        y = (screen_h // 2) - 75
        dialog.geometry(f"+{x}+{y}")
    
        tk.Label(dialog, text="Enter the hardware ID for: "+playerName, fg="cyan", bg="black",
                 font=("Arial", 15)).pack(pady=15)
    
        entry = tk.Entry(dialog, width=20, font=("Arial", 15),
                         justify="center")
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

    def run_traffic(self):
        stopVar = True
        #self.codes = {}
        counter = 0
        while stopVar:
            time.sleep(3) #sleep 3 seconds between call and response for testing and readability
            code = (self.udp_connection.recv_from())
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
                if counter == 14:
                    stopVar = False
                    self.udp_connection.send_to("221")
            except ValueError:
                print("Error in parsing int from received code")

            counter += 1

    #commented out the manual testing methods that i used. can delete them or uncomment them to test yourself - Ramon 
    """def test_base_score(self, equipment_id, base_code):
        if base_code == 43:
            self.baseScoring(equipment_id, 'green')
        elif base_code == 53:
            self.baseScoring(equipment_id, 'red')"""

    """def test_scoring(self):
        print("DEBug: f9 pressed!")
        print(f"DEBUG: equipmenttoPlayer = {self.equipmentToPlayer}")

        if hasattr(self, 'equipmentToPlayer') and self.equipmentToPlayer:
            # Test with first equipment ID
            first_equipment = list(self.equipmentToPlayer.keys())[0]
            player = self.equipmentToPlayer[first_equipment]

            print(f"debug: Testing with equipment {first_equipment}, player {player.get_player_name()}")

            # Score on opposite base
            if player.team_code == 1:  # Red team
                self.test_base_score(first_equipment, 43)  # Score on red base
            else:  # Green team
                self.test_base_score(first_equipment, 53)  # Score on green base
        else:
            print("DEBUG: No equipment mappping found")"""

if __name__ == "__main__":
    LaserTagMain()
