import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import time

# Assume these classes already exist
# from player import Player
# from player_database import PlayerDatabase
# from udp_connection import UDPConnection


class LaserTagMain:

    def __init__(self):
        self.db = PlayerDatabase()
        self.udp_connection = UDPConnection()

        # Create root window (hidden)
        self.root = tk.Tk()
        self.root.withdraw()

        # Show splash screen
        self.show_splash_screen("logo.jpg")

        # Get number of players
        num_players = self.get_number_of_players()

        # Create players
        players = []
        for i in range(1, num_players + 1):
            player_id = self.get_player_id(i)

            codename = self.db.get_codename(player_id)

            if codename is None:
                codename = simpledialog.askstring(
                    "New Player",
                    "Enter codename for new player:"
                )
                if codename is None:
                    exit()

                self.db.add_player(player_id, codename)

            # Assign team (even = Red (1), odd = Green (2))
            team_code = 1 if player_id % 2 == 0 else 2

            player = player(codename, team_code)
            players.append(player)

            # UDP communication
            self.udp_connection.send_to(player_id)
            print("Player equipment code:", self.udp_connection.recv_from())

        # Show all players
        result = "Players created:\n"
        for p in players:
            result += p.get_player_info() + "\n"

        messagebox.showinfo("Players", result)

        self.root.destroy()

    def get_number_of_players(self):
        num_players = 0
        while num_players <= 0:
            input_value = simpledialog.askstring(
                "Player Setup",
                "Enter number of players:"
            )

            if input_value is None:
                exit()

            try:
                num_players = int(input_value)
                if num_players <= 0:
                    messagebox.showerror("Error", "Number of players must be positive.")
            except ValueError:
                messagebox.showerror("Error", "Invalid number. Try again.")

        return num_players

    def get_player_id(self, player_number):
        player_id = 0
        while player_id <= 0:
            input_value = simpledialog.askstring(
                "Player Setup",
                f"Enter ID for Player {player_number}:"
            )

            if input_value is None:
                exit()

            try:
                player_id = int(input_value)
            except ValueError:
                messagebox.showerror("Error", "Invalid ID.")

        return player_id

    def show_splash_screen(self, image_path):
        splash = tk.Toplevel()
        splash.title("Splash")

        # Load and resize image
        image = Image.open(image_path)
        image = image.resize((800, 600), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(splash, image=photo)
        label.image = photo
        label.pack()

        splash.geometry("800x600")
        splash.update()

        # Center window
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        splash.geometry(f"+{x}+{y}")

        splash.after(3000, splash.destroy)  # 3 seconds
        splash.mainloop()


if __name__ == "__main__":
    LaserTagMain()
