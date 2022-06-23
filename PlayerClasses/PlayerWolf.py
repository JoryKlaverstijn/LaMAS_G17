from PlayerClasses.Player import Player
import random

class PlayerWolf(Player):
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)
        self.knows_im_wolf = []

    def get_vote(self, km, alive_player_ids):
        # We first vote anyone who knows we are a wolf
        if self.knows_im_wolf:
            return self.knows_im_wolf.pop()

        # Then we vote anyone who we know is a little girl
        targets = [idx for idx in alive_player_ids if idx != self.id]
        for idx in targets:
            if km.knows_little_girl(self.id, idx):
                return idx

        # We then kill anyone who we know is good
        for idx in targets:
            if km.knows_good(self.id, idx):
                return idx

        # Some edge case (just in case)
        return random.choice(alive_player_ids)