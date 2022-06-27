from PlayerClasses.Player import Player


class PlayerHunter(Player):
    """
    This is the class for the hunter.
    No special behaviour is added for this class.
    """
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)