from player import Player

def handle_hit(shooter, target):
    message = ""

    if shooter is None:
        message = "Invalid hit"

    elif target is None:
        message = shooter.get_player_name() + " missed."

    elif shooter.team_code == target.team_code:
        shooter.subtract_score(10)
        message = "FRIENDLY FIRE: " + shooter.get_player_name() + " hit teammate " + target.get_player_name()

    else:
        shooter.add_score(10)
        message = shooter.get_player_name() + " hit " + target.get_player_name() + " (+10)"

    return message

p1 = Player("Red1", 1)
p2 = Player("Red2", 1)
p3 = Player("Green1", 2)

print(handle_hit(p1, p2))
print(handle_hit(p1, p3))
print(handle_hit(p1, None))
    
    
    