from Game import Game
from PlayerClasses.Roles import Role
import pygame
from Button import Button
from TextChat import TextChat
from Controller import Controller
from View import View
from Colors import *

# Setup the game (max 8 players, max 1 little girl)
# HERE YOU CAN CHANGE THE AMOUNT OF PLAYERS PER ROLE!
# There should at least be 1 wolf, and 1 non-wolf role
roles = {
    Role.WOLF: 1,
    Role.VILLAGER: 7,
    Role.SEER: 1,
    Role.LITTLE_GIRL: 1,
    Role.HUNTER: 1
}
assert sum(roles.values()) <= 8, 'Too many players (should be 8 or less)'
assert roles[Role.LITTLE_GIRL] <= 1, 'Too many little girls (should be 1 or less)'

# Setup the screen and general pygame stuff
pygame.init()
res = (1000, 1000)
screen = pygame.display.set_mode(res)

text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
game = Game(roles, text_chat)

# Define the buttons
step_button = Button(x=780, y=880, w=200, h=100, text='Next step',
                     highlighted_color=LIGHT_GREEN, regular_color=DARK_GREEN)
reset_button = Button(x=780, y=620, w=200, h=100, text='Reset',
                      highlighted_color=PINK, regular_color=RED)
text_up = Button(x=720, y=580, w=20, h=30, text='^', active_func=text_chat.can_go_up,
                 highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE)
text_down = Button(x=720, y=960, w=20, h=30, text='v', active_func=text_chat.can_go_down,
                   highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE)
model_buttons = [Button(x=785 + x * 50, y=750 + y * 50, w=45, h=45, text=f'{y * 4 + x + 1}',
                        highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE, text_color=(255, 255, 255))
                        for y in range(2) for x in range(4)][:sum(roles.values())]

all_buttons = [step_button, reset_button, *model_buttons, text_up, text_down]

# Define the controller and the view instances
controller = Controller(text_chat, game, reset_button, step_button, model_buttons, text_up, text_down)
view = View(pygame)

# Main game loop
while True:
    mouse = pygame.mouse.get_pos()

    # Check for key/mouse events, and handle them
    for event in pygame.event.get():
        controller.handle_event(event, mouse, pygame)

    # Draw the game-screen
    view.draw_game(pygame, screen, game, all_buttons, mouse)
