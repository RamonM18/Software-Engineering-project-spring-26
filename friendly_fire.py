from player import Player

def handle_hit(shooter, target):
    if shooter is None or target is None:
        return "Invalid hit"
    if shooter.team_code == target.team_code:
        shooter.subtract_score(10)  
        return f"Friendy Fire: {shooter.get_player_name()} hit teammate {target.get_player_name()} (-10)"

    shooter.add_score(10)
    return f"{shooter.get_player_name()} hit {target.get_player_name()} (+10)"
    
    
    