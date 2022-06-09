from enum import Enum


class MessageType(Enum):
    IDENTITY_REVEAL = 1  # Event where the identity of a player is revealed (by Seer)
    DEATH_REPORT = 2  # A player has died (from voting, or from wolves)
    PLAYER_VOTE = 3  # A player has voted for a player to die


class Message:
    """
    A class for instantiating a message.
    Each message contains information that can be supplied to a player to inform them.
    The information can be of an event, or a message from another player to try and persuade them.
    """
    def __init__(self, players, message_type, extra_content=None):
        self.players = players
        self.message_type = message_type
        self.extra_content = extra_content
