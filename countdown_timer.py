import tkinter as tk

def countdown_timer(seconds = 30):
    window = tk.Toplevel()
    window.title("Game Countdown")
    window.configure(bg = "black")
    window.geometry("500x250")

    title = tk.Label(
        window,
        text="GAME STARTING IN",
        fg="yellow",
        bg="black",
        font=("Arial", 26, "bold")
    )
    title.pack(pady = 20)

    timer_label = tk.Label(
        window,
        text="0:30",
        fg="white",
        bg="black",
        font=("Arial", 72, "bold")
    )
    timer_label.pack()

    def update(time_left):

        minutes = time_left // 60
        seconds = time_left % 60

        timer_label.config(text = f"{minutes}:{seconds:02}")

        if time_left > 0:
            window.after(1000, update, time_left - 1)
        else:
            timer_label.config(text = "GO!")

    update(seconds)

   
