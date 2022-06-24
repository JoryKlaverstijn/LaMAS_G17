from PlayerClasses.Player import Player


class PlayerLittlegirl(Player):
    def __init__(self, name, role, roles, player_id):
        super().__init__(name, role, roles, player_id)
        self.has_peaked = False
