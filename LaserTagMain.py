import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Assume these exist
# from player import Player
# from player_database import PlayerDatabase
# from udp_connection import UDPConnection


class LaserTagMain:

    def __init__(self):

        self.db = PlayerDatabase()
        self.udp_connection = UDPConnection()

        self.root = tk.Tk()
        self.root.withdraw()

        self.show_splash_screen("logo.jpg")

        self.root.deiconify()
        self.root.title("Edit Current Game")
        self.root.configure(bg="black")
        self.root.geometry("1000x700")

        self.build_interface()

        self.root.bind("<F1>", lambda e: self.edit_game())
        self.root.bind("<F2>", lambda e: self.parameters())
        self.root.bind("<F3>", lambda e: self.start_game())
        self.root.bind("<F5>", lambda e: self.preentered())
        self.root.bind("<F8>", lambda e: self.view_game())
        self.root.bind("<F10>", lambda e: self.sync())
        self.root.bind("<F12>", lambda e: self.clear())

        self.root.mainloop()

    def build_interface(self):

        title = tk.Label(self.root, text="Edit Current Game",
                         fg="cyan", bg="black",
                         font=("Arial", 20))
        title.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack()

        # RED TEAM
        red_frame = tk.Frame(main_frame, bg="#330000")
        red_frame.grid(row=0, column=0, padx=40)

        tk.Label(red_frame, text="RED TEAM",
                 fg="white", bg="#550000",
                 font=("Arial", 14)).grid(row=0, column=0, columnspan=3, sticky="ew")

        # GREEN TEAM
        green_frame = tk.Frame(main_frame, bg="#003300")
        green_frame.grid(row=0, column=1, padx=40)

        tk.Label(green_frame, text="GREEN TEAM",
                 fg="white", bg="#005500",
                 font=("Arial", 14)).grid(row=0, column=0, columnspan=3, sticky="ew")

        self.red_entries = []
        self.green_entries = []

        for i in range(20):

            tk.Label(red_frame, text=i, fg="white", bg="#330000").grid(row=i+1, column=0)

            rid = tk.Entry(red_frame, width=10)
            rcode = tk.Entry(red_frame, width=12)

            rid.grid(row=i+1, column=1)
            rcode.grid(row=i+1, column=2)

            self.red_entries.append((rid, rcode))

            tk.Label(green_frame, text=i, fg="white", bg="#003300").grid(row=i+1, column=0)

            gid = tk.Entry(green_frame, width=10)
            gcode = tk.Entry(green_frame, width=12)

            gid.grid(row=i+1, column=1)
            gcode.grid(row=i+1, column=2)

            self.green_entries.append((gid, gcode))

        # Buttons
        bottom = tk.Frame(self.root, bg="black")
        bottom.pack(pady=20)

        buttons = [
            ("F1 Edit Game", self.edit_game),
            ("F2 Game Parameters", self.parameters),
            ("F3 Start Game", self.start_game),
            ("F5 PreEntered Games", self.preentered),
            ("F8 View Game", self.view_game),
            ("F10 Flick Sync", self.sync),
            ("F12 Clear Game", self.clear)
        ]

        for text, cmd in buttons:
            b = tk.Button(bottom, text=text, width=16, command=cmd)
            b.pack(side="left", padx=5)

    def collect_players(self):

        players = []

        # RED TEAM
        for rid, rcode in self.red_entries:

            pid = rid.get()
            code = rcode.get()

            if pid:

                pid = int(pid)

                if not code:
                    code = self.db.get_codename(pid)

                    if code is None:
                        code = "Player" + str(pid)
                        self.db.add_player(pid, code)

                player = Player(code, 1)
                players.append(player)

        # GREEN TEAM
        for gid, gcode in self.green_entries:

            pid = gid.get()
            code = gcode.get()

            if pid:

                pid = int(pid)

                if not code:
                    code = self.db.get_codename(pid)

                    if code is None:
                        code = "Player" + str(pid)
                        self.db.add_player(pid, code)

                player = Player(code, 2)
                players.append(player)

        return players

    def start_game(self):

        players = self.collect_players()

        if not players:
            messagebox.showerror("Error", "No players entered.")
            return

        for p in players:

            try:
                self.udp_connection.send_to(p.get_player_id())
                response = self.udp_connection.recv_from()
                print("Equipment code:", response)

            except Exception as e:
                print("UDP error:", e)

        result = "Players in game:\n\n"

        for p in players:
            result += p.get_player_info() + "\n"

        messagebox.showinfo("Game Started", result)

    def edit_game(self):
        print("Edit Game")

    def parameters(self):
        print("Game Parameters")

    def preentered(self):
        print("Preentered Games")

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

    def show_splash_screen(self, image_path):

        splash = tk.Toplevel()
        splash.title("Splash")

        image = Image.open(image_path)
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
        splash.mainloop()


if __name__ == "__main__":
    LaserTagMain()
