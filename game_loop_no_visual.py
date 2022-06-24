from Game import Game
from PlayerClasses.Roles import Role
from TextChat import TextChat
from Colors import *
import matplotlib.pyplot as plt

# Setup the game (max 8 players)
# HERE YOU CAN CHANGE THE AMOUNT OF PLAYERS PER ROLE!
# There should at least be 1 wolf, and 1 non-wolf role
roles = {
    Role.WOLF: 2,
    Role.VILLAGER: 1,
    Role.SEER: 2,
    Role.LITTLE_GIRL: 0,
    Role.HUNTER: 1
}
assert sum(roles.values()) <= 8, 'Too many players (should be 8 or less)'


text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
game = Game(roles, text_chat)

# Main game loop
wins = [0, 0]
for i in range(100):
    game.reset()
    while True:
        if game.game_over():
            if game.game_over() == 'Wolves':
                wins[0] += 1
            else:
                wins[1] += 1
            break
        game.step()
    print(i)

plt.bar(['Wolves', 'Villagers'], wins)
plt.ylabel('Wins')
plt.show()
