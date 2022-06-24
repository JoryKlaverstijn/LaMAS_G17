from PlayerClasses.Player import Player
import random


class PlayerSeer(Player):
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)

    # Chose which player's role to reveal
    def choose_player_to_reveal(self, alive_player_ids):
        targets = [idx for idx in alive_player_ids if idx != self.id]
        # We first try to identify anyone who is suspected to be a wolf, but is not known to be a wolf
        for idx in targets:
            if not self.km.knows_wolf(self.id, idx) and self.km.suspects(self.id, idx):
                return idx

        # Otherwise we identify a random person that we don't know the identity of
        for idx in targets:
            if not self.km.knows_wolf(self.id, idx) and not self.km.knows_little_girl(self.id, idx)\
                    and not self.km.knows_good(self.id, idx):
                return idx

        # Otherwise we just identify someone we already know the identity of
        return random.choice(targets)