import time

def countdown_timer():
    for i in range(30, 0, -1):
        print(f"Game starts in {i} seconds")
        time.sleep(1)

    print("GAME START!")

countdown_timer()