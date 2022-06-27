from Game import Game
from PlayerClasses.Roles import Role
from TextChat import TextChat
from Colors import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

# Amount of games to run
N_GAMES = 1000

# RUN EVERYTHING OVER 1000 ITERATIONS

def set_roles(roles_counts):
    roles = {
        Role.WOLF: roles_counts[0],
        Role.VILLAGER: roles_counts[1],
        Role.SEER: roles_counts[2],
        Role.LITTLE_GIRL: roles_counts[3],
        Role.HUNTER: roles_counts[4]
    }
    assert sum(roles.values()) <= 8, 'Too many players (should be 8 or less)'
    assert roles[Role.LITTLE_GIRL] <= 1, 'Too many little girls (should be 1 or 0)'

    return roles

def run_n_games_def(roles):
    # Setup the game
    text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
    game = Game(roles, text_chat)

    # Run the games, count the (correct) votes, and the wins for both teams
    wins = [0, 0]
    vote_total = 0
    correct_vote_total = 0

    for i in tqdm(range(N_GAMES)):
        wins, vote_total, correct_vote_total = run_one_game(game, wins, vote_total, correct_vote_total)

    return wins, vote_total, correct_vote_total

def run_n_games_lg(roles):
    det_percent = np.linspace(0.1, 1.0, 10)
    det_percent_wins = [0]*len(det_percent)
    games_per_perc = int(N_GAMES/len(det_percent))

    # Setup the game
    text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
    game = Game(roles, text_chat)

    # Run the games, count the (correct) votes, and the wins for both teams
    vote_total = 0
    correct_vote_total = 0

    for idx, det_perc in enumerate(det_percent):
        for i in tqdm(range(games_per_perc)):
            wins = [0, 0]
            game.set_little_girl_detection_chance(det_perc)
            wins, vote_total, correct_vote_total = run_one_game(game, wins, vote_total, correct_vote_total)
            if wins[1] == 1:
                det_percent_wins[idx] += 1
    
    return det_percent, det_percent_wins, vote_total, correct_vote_total

def run_one_game(game, wins, vote_total, correct_vote_total):
    game.reset()
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

    return wins, vote_total, correct_vote_total

def print_bar_res(wins, correct_vote_total, vote_total, name):    
    # Printing graphs
    plt.bar(['Wolves', 'Villagers'], wins, color=['red', 'blue'])
    plt.ylabel('Amount of wins')
    plt.ylim(0, N_GAMES)
    plt.savefig('results/' + str(name) + '_bar_graph_' + str(N_GAMES) + '_iterations.png')
    plt.clf()

def print_little_girl_res(det_percent, det_percent_wins, vote_total, correct_vote_total):
    # Results from plotting girl detection chances  
    print("Detect percentage wins: " + str(det_percent_wins))
    print(f'Correct votes: {correct_vote_total}/{vote_total} -> {correct_vote_total / vote_total * 100:.4f}%')

    # Printing graphs
    plt.plot(det_percent, list(reversed(det_percent_wins)))
    plt.ylabel('Villager wins')
    plt.xlabel('Little girl detection chance')
    plt.ylim(0, int(N_GAMES/10))
    plt.savefig('results/Little_girl_detection_res_' + str(N_GAMES) + '_iterations.png')
    plt.clf()

def main():
    def_roles = set_roles([2, 3, 1, 1, 1])
    res = []

    # Getting the little girl detect percentage results
    det_percent, det_percent_wins, vote_total, correct_vote_total = run_n_games_lg(def_roles)
    print_little_girl_res(det_percent, det_percent_wins, vote_total, correct_vote_total)

    # Different distributions of roles
    # default = [wolf, wolf, villager, villager, villager, seer, little girl, hunter]
    # more_seers = [wolf, wolf, villager, villager, seer, seer, little girl, hunter]
    # more_hunters = [wolf, wolf, villager, villager, hunter, seer, little girl, hunter]
    # more_wolves = [wolf, wolf, wolf, seer, seer, seer, little girl, hunter]

    # Runtime: ~7.5 hours for 1000 iterations
    # Getting the different role distribution results
    # for name, role_set in [["default", [2, 3, 1, 1, 1]], ["more_seers", [2, 2, 2, 1, 1]], ["more_hunters", [2, 2, 1, 1, 2]], ["more_wolves", [3, 0, 3, 1, 1]]]:
    #     wins, vote_total, correct_vote_total = run_n_games_def(set_roles(role_set))
    #     res.append([name, wins, vote_total, correct_vote_total])
    #     print_bar_res(wins, vote_total, correct_vote_total, name)
    
    # for name, wins, vote_total, correct_vote_total in res:
    #     print("Name of role set = " + str(name))
    #     print("Wolves and villager wins: " + str(wins))
    #     print(f'Correct votes: {correct_vote_total}/{vote_total} -> {correct_vote_total / vote_total * 100:.4f}%')

if __name__ == "__main__":
    main()
