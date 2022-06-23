from PlayerClasses.Roles import Role
from PlayerClasses.PlayerWolf import PlayerWolf
from PlayerClasses.PlayerVillager import PlayerVillager
from PlayerClasses.PlayerSeer import PlayerSeer
from PlayerClasses.PlayerLittlegirl import PlayerLittlegirl
from PlayerClasses.PlayerHunter import PlayerHunter
from mlsolver.model import MillerHollowModel
from enum import Enum
from Message import MessageType, Message
import random


class State(Enum):
    START = 1
    WOLVES_IDENTIFY_EACH_OTHER = 2
    SETUP_SEER_TURN = 3
    SEER_TURN = 4
    SETUP_VOTING_DAY = 5
    VOTING_DAY = 6
    VOTING_DAY_RESULTS = 7
    WOLF_SETUP = 8
    VOTING_NIGHT = 9
    VOTING_NIGHT_RESULTS = 10
    SETUP_HUNTER_PAYBACK = 11
    HUNTER_PAYBACK = 12
    LITTLE_GIRL_PEEKS = 13
    LITTLE_GIRL_CAUGHT = 14


class Game:
    """
    This class holds the state of the game and controls the progress of the game.
    """
    role_class_mapping = {
        Role.WOLF: PlayerWolf,
        Role.VILLAGER: PlayerVillager,
        Role.SEER: PlayerSeer,
        Role.LITTLE_GIRL: PlayerLittlegirl,
        Role.HUNTER: PlayerHunter,
    }

    def __init__(self, roles, text_chat):
        self.text_chat = text_chat
        self.players_to_vote = self.seers = self.votes = self.players = None
        self.roles = roles
        self.initialize_players()
        self.km = MillerHollowModel(self.players)
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

    def game_over(self):
        """
        Checks if the game is won, and if it is, it returns the winner
        """
        wolf_count = len([player for player in self.players if player.role == Role.WOLF and player.alive])
        villager_count = len([player for player in self.players if player.role != Role.WOLF and player.alive])
        if villager_count == 0:
            return 'Wolves'
        elif wolf_count == 0:
            return 'Villagers'
        else:
            return False

    def start(self):
        # The game has just started
        self.text_chat.add_message("The game has started, and everyone knows their own identity.", (255, 255, 0))
        self.state = State.WOLVES_IDENTIFY_EACH_OTHER

    def wolfs_identify_each_other(self):
        """
        Inform all wolves who the other wolves are.
        """
        wolves = [idx for idx in range(len(self.players)) if self.players[idx].role == Role.WOLF]
        for idx1 in wolves:
            for idx2 in wolves:
                if idx1 != idx2:
                    self.km.update_knows_wolf(idx1, idx2)

        self.text_chat.add_message("The wolves now know who the other wolves are.", (255, 255, 0))
        self.state = State.SETUP_SEER_TURN

    def setup_seer_turn(self):
        """
        Setups the list of seers that are allowed to reveal an identity.
        """
        self.text_chat.add_message("It is now the turn of the seers to identify another player's role.", (255, 255, 0))
        self.seers = [player for player in self.players if player.role == Role.SEER and player.alive]
        self.alive_players = [player.id for player in self.players if player.alive]
        random.shuffle(self.seers)
        self.state = State.SEER_TURN

    def seer_turn(self):
        """
        Each seer is now allowed to reveal a chosen person's identity
        """
        if not self.seers:
            self.text_chat.add_message("All living seers have identified someone's role.", (255, 255, 0))
            self.state = State.WOLF_SETUP
            return

        seer = self.seers.pop()
        random.shuffle(self.alive_players)
        chosen_player = self.players[seer.choose_player_to_reveal(self.km, self.alive_players)]
        if chosen_player.role == Role.WOLF:
            self.km.update_knows_wolf(seer.id, chosen_player.id)
        elif chosen_player.role == Role.LITTLE_GIRL:
            self.km.update_knows_little_girl(seer.id, chosen_player.id)
        else:
            self.km.update_knows_good(seer.id, chosen_player.id)
        self.text_chat.add_message(
            f"{seer.name} has identified the role of {chosen_player.name}" +
            f" ({str(chosen_player.role)[5:]})", (196, 196, 196))

    def wolf_setup(self):
        """
        Setup of the night of the wolves.
        """
        self.text_chat.add_message("The wolves are about to vote to kill someone...",
                                   (255, 255, 0))
        self.players_to_vote = [player for player in self.players if player.role == Role.WOLF and player.alive]
        self.alive_players = [player.id for player in self.players if player.alive]
        self.votes = [0 for _ in range(len(self.players))]

        random.shuffle(self.players_to_vote)
        self.state = State.VOTING_NIGHT

    def voting_night(self):
        """
        The wolves get to vote to kill one of the villagers.
        """
        if not self.players_to_vote:
            for player in self.players:
                if player.alive:
                    player.voted = False
            self.text_chat.add_message("All wolves have voted...", (255, 255, 0))
            self.state = State.VOTING_NIGHT_RESULTS
            return

        voting_player = self.players_to_vote.pop()
        voting_player.voted = True
        random.shuffle(self.alive_players)
        voted_player = self.players[voting_player.get_vote(self.km, self.alive_players)]
        self.votes[voted_player.id] += 1
        total_to_vote = len([player for player in self.players if player.alive and player.role == Role.WOLF])
        self.text_chat.add_message(
            f"{voting_player.name} has voted to kill {voted_player.name} ({sum(self.votes)}/{total_to_vote})",
            (255, 128, 128)
        )

    def voting_night_results(self):
        """
        Inform all players which villager is killed by the wolves during the night.
        """
        max_voted_players = [idx for idx, cnt in enumerate(self.votes) if cnt == max(self.votes)]
        player_to_die = self.players[random.choice(max_voted_players)]
        self.text_chat.add_message(
            f"The wolves have voted for {player_to_die.name} to die, they were a {str(player_to_die.role)[5:]}!", (196, 40, 40)
        )
        player_to_die.alive = False
        for player in self.players:
            if player.alive:
                if player_to_die.role == Role.LITTLE_GIRL:
                    self.km.update_knows_little_girl(player.id, player_to_die.id)
                else:
                    self.km.update_knows_good(player.id, player_to_die.id)

        if player_to_die.role == Role.HUNTER:
            self.previous_state = State.VOTING_NIGHT_RESULTS
            self.state = State.SETUP_HUNTER_PAYBACK
            self.killed_hunter = player_to_die
        else:
            self.state = State.SETUP_VOTING_DAY

    def setup_voting_day(self):
        self.text_chat.add_message("All players are about to vote for someone to die.", (255, 255, 0))
        self.votes = [0 for _ in range(len(self.players))]
        self.players_to_vote = [player for player in self.players if player.alive]
        self.alive_players = [player.id for player in self.players if player.alive] # We need an extra copy
        random.shuffle(self.players_to_vote)
        self.state = State.VOTING_DAY

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
        random.shuffle(self.alive_players)
        voted_player = self.players[voting_player.get_vote(self.km, self.alive_players)]
        self.votes[voted_player.id] += 1
        voted_amnt = sum(self.votes)
        total_to_vote = len(self.alive_players)
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
            f"The players have voted for {player_to_die.name} to die, they were a {str(player_to_die.role)[5:]}!", (196, 40, 40)
        )
        player_to_die.alive = False
        for player in self.players:
            if player.alive:
                if player_to_die.role == Role.WOLF:
                    self.km.update_knows_wolf(player.id, player_to_die.id)
                elif player_to_die.role == Role.LITTLE_GIRL:
                    self.km.update_knows_little_girl(player.id, player_to_die.id)
                else:
                    self.km.update_knows_good(player.id, player_to_die.id)

        if player_to_die.role == Role.HUNTER:
            self.previous_state = State.VOTING_DAY_RESULTS
            self.state = State.SETUP_HUNTER_PAYBACK
            self.killed_hunter = player_to_die
        else:
            if any(player.role == Role.SEER and player.alive for player in self.players):
                self.state = State.SETUP_SEER_TURN
            else:
                self.state = State.WOLF_SETUP

    def setup_hunter_payback(self):
        self.text_chat.add_message(
            f"The person that died was a hunter and is about to shoot someone...",
            (255, 255, 0)
        )
        self.state = State.HUNTER_PAYBACK

    def hunter_payback(self):
        player_to_die = self.players[self.killed_hunter.get_vote(self.km, self.alive_players)]
        player_to_die.alive = False
        for player in self.players:
            if player.alive:
                if player_to_die.role == Role.WOLF:
                    self.km.update_knows_wolf(player.id, player_to_die.id)
                elif player_to_die.role == Role.LITTLE_GIRL:
                    self.km.update_knows_little_girl(player.id, player_to_die.id)
                else:
                    self.km.update_knows_good(player.id, player_to_die.id)
        self.text_chat.add_message(
            f"The hunter has chosen to shoot {player_to_die.name}, they were a {str(player_to_die.role)[5:]}!",
            (196, 40, 40)
        )

        # If the shot player is a hunter, then it is allowed to shoot as well
        if player_to_die.role == Role.HUNTER:
            self.state = State.SETUP_HUNTER_PAYBACK
            self.killed_hunter = player_to_die
        else:
            # No hunter has been harmed, we continue with either day or night voting
            if self.previous_state == State.VOTING_DAY_RESULTS:
                if any(player.role == Role.SEER and player.alive for player in self.players):
                    self.state = State.SETUP_SEER_TURN
                else:
                    self.state = State.WOLF_SETUP
            else:
                self.state = State.SETUP_VOTING_DAY

    def little_girl_peeks(self):
        self.text_chat.add_message(
            f"The little girl peeks and now knows the identity of the wolves.",
            (255, 255, 0)
        )

        if random.random() < 0.4:
            self.state = State.LITTLE_GIRL_CAUGHT
        else:
            self.state = State.SETUP_VOTING_DAY

    def little_girl_caught(self):
        self.text_chat.add_message(
            f"The little girl got caught, and the wolves know her identity.",
            (255, 255, 0)
        )

        self.state = State.SETUP_VOTING_DAY

    def step(self):
        """
        Is called when the game should progress. Calls the appropriate function depending on current state.
        """
        step_methods = {
            State.START: self.start,
            State.WOLVES_IDENTIFY_EACH_OTHER: self.wolfs_identify_each_other,
            State.SETUP_SEER_TURN: self.setup_seer_turn,
            State.SEER_TURN: self.seer_turn,
            State.SETUP_VOTING_DAY: self.setup_voting_day,
            State.VOTING_DAY: self.voting_day,
            State.VOTING_DAY_RESULTS: self.voting_day_results,
            State.WOLF_SETUP: self.wolf_setup,
            State.VOTING_NIGHT: self.voting_night,
            State.VOTING_NIGHT_RESULTS: self.voting_night_results,
            State.SETUP_HUNTER_PAYBACK: self.setup_hunter_payback,
            State.HUNTER_PAYBACK: self.hunter_payback,
            State.LITTLE_GIRL_PEEKS: self.little_girl_peeks,
            State.LITTLE_GIRL_CAUGHT: self.little_girl_caught,
        }

        # Run the appropriate method
        step_methods[self.state]()

    def reset(self):
        """
        Resets the state of the game.
        """
        self.text_chat.reset()
        self.initialize_players()
        self.km.setup(self.players)
        self.state = State.START
