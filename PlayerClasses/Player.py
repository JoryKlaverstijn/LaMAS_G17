import random
from PlayerClasses.Roles import Role

class Player:
    """
    The main parent class of all players.
    Has a get_vote and tell_role method which are only used by all good roles
    """
    def __init__(self, name, role, roles, player_id):
        self.name = name
        self.role = role
        self.alive = True
        self.roles = roles
        self.voted = False
        self.id = player_id

    def get_vote(self, alive_player_ids):
        """
        Gets the ids of the players that are still alive, and votes which one should die.
        returns the index of the player that we want to vote out.
        """
        targets = [idx for idx in alive_player_ids if idx != self.id]
        # Villagers try to vote for someone they know is a wolf
        for idx in targets:
            if self.km.knows_wolf(self.id, idx):
                return idx

        # Then villagers try to vote someone that they have not confirmed is not a wolf
        for idx in targets:
            if self.km.suspects(self.id, idx):
                return idx

        # If the villager has no useful knowledge, they vote randomly
        print('aaah')
        return random.choice(targets)

    def tell_role(self, alive_player_ids):
        """
        Goes through knowledge base and checks if we have useful knowledge to tell others.
        Returns None if no useful info, otherwise the index of the player with their role.
        """
        other_players_ids = [idx for idx in alive_player_ids if idx != self.id]

        # The most important thing to share is who is the wolf
        # If we know who the wolf is, and we don't know that someone knows that person is a wolf, we share it
        for idx1 in other_players_ids:
            if self.km.knows_wolf(self.id, idx1):
                for idx2 in other_players_ids:
                    if not self.km.knows_wolf(idx2, idx1):
                        return (idx1, Role.WOLF)

        # If we don't know who the wolf is, or everyone already knows, we try to share who is the little girl
        for idx1 in other_players_ids:
            if self.km.knows_little_girl(self.id, idx1):
                for idx2 in other_players_ids:
                    if not self.km.knows_little_girl(idx2, idx1):
                        return (idx1, Role.LITTLE_GIRL)

        # Finally we try to share who is good (no wolf)
        for idx1 in other_players_ids:
            if self.km.knows_good(self.id, idx1):
                for idx2 in other_players_ids:
                    if not self.km.knows_good(idx2, idx1):
                        # We return villager role here, but the player can be any non-wolf, non-girl role
                        return (idx1, Role.VILLAGER)

        # We don't have much useful knowledge, we share nothing
        return None
