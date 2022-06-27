from PlayerClasses.Player import Player
import random

class PlayerWolf(Player):
    """
    This is the class of the wolf.
    The wolf has a different way of voting.
    The wolf wants to kill all good roles, not other wolves.
    """
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)
        self.km = None

    def get_vote(self, alive_player_ids):
        targets = [idx for idx in alive_player_ids if idx != self.id]
        # We first vote anyone who we know knows our role
        for idx in targets:
            if self.km.knows_wolf(idx, self.id) and not self.km.knows_wolf(self.id, idx):
                return idx

        # Then we vote anyone who we know is a little girl
        for idx in targets:
            if self.km.knows_little_girl(self.id, idx):
                return idx

        # We then kill anyone who we know is good
        for idx in targets:
            if self.km.knows_good(self.id, idx):
                return idx

        # Some edge case (just in case)
        return random.choice(alive_player_ids)