from Game import Game
from PlayerClasses.Roles import Role
from TextChat import TextChat
from Colors import *
import matplotlib.pyplot as plt
from multiprocessing import Pool

# Amount of games to run
N_GAMES = 1000

# Setup the game (max 8 players)
# HERE YOU CAN CHANGE THE AMOUNT OF PLAYERS PER ROLE!
# There should at least be 1 wolf, and 1 non-wolf role
roles = {
    Role.WOLF: 2,
    Role.VILLAGER: 3,
    Role.SEER: 1,
    Role.LITTLE_GIRL:1,
    Role.HUNTER: 1
}

assert sum(roles.values()) <= 8, 'Too many players (should be 8 or less)'
assert roles[Role.LITTLE_GIRL] <= 1, 'Too many little girls (should be 1 or 0)'

def play_game(x):
    # Setup the game
    text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
    game = Game(roles, text_chat)
    # Run the games, count the (correct) votes, and the wins for both teams
    wins = [0, 0]
    vote_total = 0
    correct_vote_total = 0
    while True:
        if game.game_over():
            if game.game_over() == 'Wolves':
                wins[0] += 1
            else:
                wins[1] += 1
            vote_total += game.vote_total
            correct_vote_total += game.correct_vote_total
            break
        game.step()

    print(x)

    return wins, correct_vote_total, vote_total

if __name__ == '__main__':
    wins = [0, 0]
    correct_vote_total = 0
    vote_total = 0
    with Pool(18) as p:
        results = p.map(play_game, list(range(N_GAMES)))

        for res in results:
            wins[0] += res[0][0]
            wins[1] += res[0][1]
            correct_vote_total += res[1]
            vote_total += res[2]

    # Show results
    print(f'Correct votes: {correct_vote_total}/{vote_total} -> {correct_vote_total / vote_total * 100:.4f}%')
    print(wins)
    plt.bar(['Wolves', 'Villagers'], wins, color=['red', 'blue'])
    plt.ylabel('Wins')
    plt.show()
