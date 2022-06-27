from PlayerClasses.Player import Player


class PlayerLittlegirl(Player):
    """
    This is the class of the little girl.
    An attribute "has_peaked" is added so that we can track that the girl has peaked before.
    The girl only peeks once.
    """
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)
        self.has_peeked = False
