import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
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

        self.show_splash_screen("logo.jpg")
        time.sleep(3)
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
                    #saving entered codename to database if it doesn't exit already
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
                    #saving entered codename to database on green team if it doesn't already exist
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
        
        #equipment mapping and base scoring tracking
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
        #self.buildScreenClosed = True

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
                
        #self.root.withdraw()
        #self.buildScreenClosed = True
        self.show_play_action_screen(red_team, green_team)
        
        self.gameStarted = True
    
    def baseScoring(self, equipment_id, base_color):
        #checking if player/equipment has already hit the base 
        if equipment_id in self.base_hit:
            print("Equipment has already scored on base")
            return
        #checking if we the equipment is mapped to a player
        if equipment_id not in self.equipmentToPlayer:
            print("Unknown equipment ID")
            return

        player = self.equipmentToPlayer[equipment_id]

        #Seeing what team scored on the base
        if base_color == 'green' and player.team_code == 2:
            print(f"{player.get_player_name()} cannot score on own base!")
            return
        if base_color == 'red' and player.team_code == 1:
            print(f"{player.get_player_name()} cannot score on own base!")
            return
        
        #giving points
        player.add_score(100)
        self.base_hit.add(equipment_id)

        print(f"{player.get_player_name()} scored 100 points on {base_color} base!")

        #calling update player to show icon
        self.update_playerDisplay(player)
    
    #method to update team scores
    def updateTeamScores(self):
        red_total = 0
        green_total = 0

        for player, label in self.player_labels.items():
            if player.team_code == 1: #Red
                red_total += player.get_score()
            else:
                green_total += player.get_score()

        self.red_score_label.config(text=str(red_total))
        self.green_score_label.config(text=str(green_total))

    #updating player label to show base icon jpg
    def update_playerDisplay(self, player):
        if player in self.player_labels:
            label = self.player_labels[player]

            #load base icon
            try:
                icon = Image.open("baseicon.jpg")
                icon = icon.resize((20,20), Image.LANCZOS) #making it small
                icon_photo = ImageTk.PhotoImage(icon)

                #updating label to show icon
                label.config(text=f"{player.get_player_name()} - {player.get_score()}", image=icon_photo, compound = 'left')
                label.image = icon_photo

            except Exception as e:
                print("Error loading base icon")

        self.updateTeamScores()
        
    def show_play_action_screen(self, red_team, green_team):

        #store player labels for updating
        self.player_labels = {} #Maps player object to their label

        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Current Game Action")
        self.game_window.configure(bg="black")
        self.game_window.geometry("900x600")
        self.game_window.bind("<F5>", lambda e: self.display_switch()) #Ensures f5 key still works
        #self.game_window.bind("<F9>", lambda e: self.test_scoring()) #used this as a manual test for the base icon, can uncomment or delete later -Ramon

         # Bring back main window when game window closes
        def on_close():
            self.game_window.destroy()
            self.root.deiconify() #Show main window again
        self.game_window.protocol("WM_DELETE_WINDOW", on_close)

        score_frame = tk.Frame(self.game_window, bg="black")
        score_frame.pack(pady=10)

        red_frame = tk.Frame(score_frame, bg="black")
        red_frame.pack(side="left", padx=80)

        tk.Label(red_frame, text="RED TEAM", fg="red", bg="black", font=("Arial", 16)).pack()
        self.red_score_label = tk.Label(red_frame, text="0", fg="red", bg="black", font=("Arial", 20))
        self.red_score_label.pack()
        for p in red_team:
            player_label = tk.Label(red_frame, text=f"{p.get_player_name()} - {p.get_score()}", fg="white", bg="black")
            player_label.pack()
            self.player_labels[p] = player_label


        green_frame = tk.Frame(score_frame, bg="black")
        green_frame.pack(side="right", padx=80)

        tk.Label(green_frame, text="GREEN TEAM", fg="lime", bg="black", font=("Arial", 16)).pack()
        self.green_score_label = tk.Label(green_frame, text="0", fg="lime", bg="black", font=("Arial", 20))
        self.green_score_label.pack()

        for p in green_team:
            player_label = tk.Label(green_frame, text=f"{p.get_player_name()} - {p.get_score()}", fg="white", bg="black")
            player_label.pack()
            self.player_labels[p] = player_label

        action_frame = tk.Frame(self.game_window, bg="black")
        action_frame.pack(pady=20)

        tk.Label(action_frame, text="Current Game Action",
                 fg="white", bg="black", font=("Arial", 14)).pack()

        action_log = tk.Text(action_frame,
                             width=70,
                             height=15,
                             bg="navy",
                             fg="white")
        action_log.pack()

        timer_label = tk.Label(self.game_window,
                               text="Time Remaining: 6:00",
                               fg="white",
                               bg="black",
                               font=("Arial", 16))
        timer_label.pack(pady=10)

        self.buildScreen = False

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
        
        dialog.update_idletasks()
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        x = (screen_w // 2) - 150
        y = (screen_h // 2) - 75
        dialog.geometry(f"+{x}+{y}")
    
        tk.Label(dialog, text="Enter the hardware ID for: "+playerName, fg="cyan", bg="black",
                 font=("Arial", 12)).pack(pady=15)
    
        entry = tk.Entry(dialog, width=20, font=("Arial", 12),
                         justify="center")
        entry.pack()
        entry.focus_set()  # Auto-focus the entry box
    
        def submit():
            try:
                result[0] = int(entry.get())
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer.", parent=dialog)
                entry.delete(0, tk.END)
    
        def on_enter(event):
            submit()
    
        entry.bind("<Return>", on_enter)  # Allow Enter key to submit
        tk.Button(dialog, text="OK", width=10, command=submit).pack(pady=10)
    
        dialog.wait_window()  # Wait until dialog closes before returning
        return result[0]

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

        splash.update()

        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()

        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)

        splash.geometry(f"+{x}+{y}")

        splash.after(3000, splash.destroy)
    
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
