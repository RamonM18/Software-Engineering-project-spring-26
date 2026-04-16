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
    
    
    