from PlayerClasses.Player import Player
import random


class PlayerSeer(Player):
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)

    # Chose which player's role to reveal
    def choose_player_to_reveal(self):
        return random.randrange(sum(self.roles.values()))
