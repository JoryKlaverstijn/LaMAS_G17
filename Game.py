from PlayerClasses.Roles import Role
from PlayerClasses.PlayerWolf import PlayerWolf
from PlayerClasses.PlayerVillager import PlayerVillager
from PlayerClasses.PlayerSeer import PlayerSeer
from PlayerClasses.PlayerLittlegirl import PlayerLittlegirl
from enum import Enum
from Message import MessageType, Message
from itertools import combinations
import random


class State(Enum):
    START = 1
    WOLF_REVEAL_EACH_OTHER = 2
    SETUP_SEER_TURN = 3
    SEER_TURN = 4
    VOTING_DAY = 5
    VOTING_DAY_RESULTS = 6
    WOLF_COMMUNICATE = 7
    VOTING_NIGHT = 8
    VOTING_NIGHT_RESULTS = 9


class Game:
    """
    This class holds the state of the game and controls the progress of the game.
    """
    role_class_mapping = {
        Role.WOLF: PlayerWolf,
        Role.VILLAGER: PlayerVillager,
        Role.SEER: PlayerSeer,
        Role.LITTLE_GIRL: PlayerLittlegirl,
    }

    def __init__(self, roles, text_chat):
        self.text_chat = text_chat
        self.players_to_vote = self.seers = self.votes = self.players = None
        self.roles = roles
        self.initialize_players()
        self.state = State.START

    def initialize_players(self):
        """
        Creates instances of players using the distribution of roles. Also gives each player a random name.
        """
        # Load some random names for the players
        with open('names.csv', 'r') as f:
            names = f.read().split('\n')
            random.shuffle(names)
            names = names[:sum(self.roles.values())]

        # Initialize the players with their role, name and the role distribution
        player_id = 0
        self.players = []
        for role, amount in self.roles.items():
            for _ in range(amount):
                player_class = Game.role_class_mapping[role]
                self.players.append(player_class(names[player_id], role, self.roles, player_id))
                player_id += 1

        for idx, player in enumerate(self.players):
            message = Message([idx], MessageType.IDENTITY_REVEAL, player.role)
            player.inform(message)

    def game_over(self):
        """
        Checks if the game is won, and if it is, it returns the winner
        """
        wolf_count = len([player for player in self.players if player.role == Role.WOLF and player.alive])
        villager_count = len([player for player in self.players if player.role != Role.WOLF and player.alive])
        if wolf_count >= villager_count:
            return 'Wolves'
        elif wolf_count == 0:
            return 'Villagers'
        else:
            return False

    def start(self):
        # The game has just started
        self.text_chat.add_message("The game has started, and everyone knows their own identity.", (255, 255, 0))
        self.state = State.WOLF_REVEAL_EACH_OTHER

    def wolf_reveal_each_other(self):
        """
        Inform all wolves who the other wolves are.
        """
        wolves = [(idx, player) for idx, player in enumerate(self.players) if player.role == Role.WOLF]
        for (_, wolf1), (idx, wolf2) in combinations(wolves, r=2):
            message = Message([idx], MessageType.IDENTITY_REVEAL, wolf2.role)
            wolf1.inform(message)
        self.text_chat.add_message("The wolves now know who the other wolves are.", (255, 255, 0))
        self.state = State.WOLF_COMMUNICATE

    def wolf_communicate(self):
        """
        Allow the wolves to communicate with each other before killing a villager.
        """
        self.text_chat.add_message("The wolves have communicated who they want to kill...",
                                   (255, 255, 0))
        self.players_to_vote = [player for player in self.players if player.role == Role.WOLF and player.alive]
        self.votes = [0 for _ in range(len(self.players))]
        self.state = State.VOTING_NIGHT

    def voting_night(self):
        """
        The wolves get to vote to kill one of the villagers.
        """
        if not self.players_to_vote:
            for player in self.players:
                if player.alive:
                    player.voted = False
            self.text_chat.add_message("All wolfs have voted...", (255, 255, 0))
            self.state = State.VOTING_NIGHT_RESULTS
            return

        voting_player = self.players_to_vote.pop()
        voting_player.voted = True
        voted_player = self.players[voting_player.get_vote()]
        self.votes[voted_player.id] += 1
        total_to_vote = len([player for player in self.players if player.alive and player.role == Role.WOLF])
        message = Message([voting_player.id, voted_player.id], MessageType.PLAYER_VOTE)
        for player in [player for player in self.players if player.role == Role.WOLF and player.alive]:
            if player.alive:
                player.inform(message)
        self.text_chat.add_message(
            f"{voting_player.name} has voted to kill {voted_player.name} ({sum(self.votes)}/{total_to_vote})",
            (150, 64, 64)
        )

    def voting_night_results(self):
        """
        Inform all players which villager is killed by the wolves during the night.
        """
        max_voted_players = [idx for idx, cnt in enumerate(self.votes) if cnt == max(self.votes)]
        player_to_die = self.players[random.choice(max_voted_players)]
        self.text_chat.add_message(
            f"The wolfs have voted for {player_to_die.name} to die!", (196, 40, 40)
        )
        player_to_die.alive = False
        message = Message([player_to_die.id], MessageType.DEATH_REPORT)
        for player in self.players:
            if player.alive:
                player.inform(message)

        self.state = State.SETUP_SEER_TURN

    def setup_seer_turn(self):
        """
        Setups the list of seers that are allowed to reveal an identity.
        """
        self.text_chat.add_message("It is now the turn of the seers to reveal someone's identity.", (255, 255, 0))
        self.seers = [player for player in self.players if player.role == Role.SEER and player.alive]
        self.state = State.SEER_TURN

    def seer_turn(self):
        """
        Each seer is now allowed to reveal a chosen person's identity
        """
        if not self.seers:
            self.text_chat.add_message("All living seers have revealed someone's identity.", (255, 255, 0))
            self.text_chat.add_message("It is now time to vote!", (255, 255, 0))
            self.votes = [0 for _ in range(len(self.players))]
            self.players_to_vote = [player for player in self.players if player.alive]
            self.state = State.VOTING_DAY
            return

        seer = self.seers.pop()
        chosen_player = self.players[seer.choose_player_to_reveal()]
        message = Message([chosen_player.id], MessageType.IDENTITY_REVEAL, chosen_player.role)
        seer.inform(message)
        self.text_chat.add_message(
            f"{seer.name} has revealed the identity of {chosen_player.name}" +
            f" ({str(chosen_player.role)[5:]})", (196, 196, 196))

    def voting_day(self):
        """
        Each player is allowed to vote one of the villagers/wolves to die.
        """
        if not self.players_to_vote:
            for player in self.players:
                if player.alive:
                    player.voted = False
            self.text_chat.add_message("All players have voted...", (255, 255, 0))
            self.state = State.VOTING_DAY_RESULTS
            return

        voting_player = self.players_to_vote.pop()
        voting_player.voted = True
        voted_player = self.players[voting_player.get_vote()]
        self.votes[voted_player.id] += 1
        voted_amnt = sum(self.votes)
        total_to_vote = len([player for player in self.players if player.alive])
        message = Message([voting_player.id, voted_player.id], MessageType.PLAYER_VOTE)
        for player in self.players:
            if player.alive:
                player.inform(message)
        self.text_chat.add_message(
            f"{voting_player.name} has voted to kill {voted_player.name} ({voted_amnt}/{total_to_vote})",
            (255, 128, 128)
        )

    def voting_day_results(self):
        """
        Reveal to all players who has died during the day.
        """
        max_voted_players = [idx for idx, cnt in enumerate(self.votes) if cnt == max(self.votes)]
        player_to_die = self.players[random.choice(max_voted_players)]
        self.text_chat.add_message(
            f"The players have voted for {player_to_die.name} to die!", (196, 40, 40)
        )
        player_to_die.alive = False
        message = Message([player_to_die.id], MessageType.DEATH_REPORT)
        for player in self.players:
            if player.alive:
                player.inform(message)

        self.votes = [0 for _ in range(len(self.players))]
        self.state = State.WOLF_COMMUNICATE

    def step(self):
        """
        Is called when the game should progress. Calls the appropriate function depending on current state.
        """
        step_methods = {
            State.START: self.start,
            State.WOLF_REVEAL_EACH_OTHER: self.wolf_reveal_each_other,
            State.SETUP_SEER_TURN: self.setup_seer_turn,
            State.SEER_TURN: self.seer_turn,
            State.VOTING_DAY: self.voting_day,
            State.VOTING_DAY_RESULTS: self.voting_day_results,
            State.WOLF_COMMUNICATE: self.wolf_communicate,
            State.VOTING_NIGHT: self.voting_night,
            State.VOTING_NIGHT_RESULTS: self.voting_night_results
        }

        # Run the appropriate method
        step_methods[self.state]()

    def reset(self):
        """
        Resets the state of the game.
        """
        self.text_chat.reset()
        self.initialize_players()
        self.state = State.START

