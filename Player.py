class Player:
    # Static class variable (shared across all players)
    next_player_num = 1

    def __init__(self, player_name, team_code):
        # Assign and increment static player number
        self.player_num = Player.next_player_num
        Player.next_player_num += 1

        self.player_name = player_name
        self.score = 0
        self.team_code = team_code

    # Copy constructor equivalent
    @classmethod
    def copy(cls, other_player):
        new_player = cls(other_player.player_name, other_player.team_code)
        new_player.player_num = other_player.player_num
        new_player.score = other_player.score
        return new_player

    # Getters
    def get_player_name(self):
        return self.player_name

    def get_player_num(self):
        return self.player_num

    def get_score(self):
        return self.score

    @classmethod
    def get_next_player_num(cls):
        return cls.next_player_num

    def get_team(self):
        if self.team_code == 1:
            return "Red"
        elif self.team_code == 2:
            return "Green"
        else:
            return "Unassigned"

    # Setters
    def set_score(self, score):
        self.score = score

    def set_player_num(self, player_num):
        self.player_num = player_num

    # Score modifiers
    def add_score(self, points):
        self.score += points

    def subtract_score(self, points):
        self.score -= points

    def get_player_info(self):
        return (
            f"Player Number: {self.player_num}, "
            f"Name: {self.player_name}, "
            f"Score: {self.score}, "
            f"Team: {self.get_team()}"
        )

    # Optional: helpful for printing directly
    def __str__(self):
        return self.get_player_info()
