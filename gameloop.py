from Game import Game
from PlayerClasses.Roles import Role
import pygame
from Button import Button
from TextChat import TextChat
from Controller import Controller
from View import View
from Colors import *


# Setup the game (max 8 players)
# HERE YOU CAN CHANGE THE AMOUNT OF PLAYERS PER ROLE!
# There should at least be 1 wolf, and 1 non-wolf role
roles = {
    Role.WOLF: 2,
    Role.VILLAGER: 3,
    Role.SEER: 2,
    Role.LITTLE_GIRL: 1
}
assert sum(roles.values()) <= 8, 'Too many players (should be 8 or less)'

# Setup the screen and general pygame stuff
pygame.init()
res = (1000, 1000)
screen = pygame.display.set_mode(res)

text_chat = TextChat(x=20, y=580, w=720, h=410, bg_color=BLUE_GRAY)
game = Game(roles, text_chat)

# Define the buttons
step_button = Button(x=780, y=880, w=200, h=100,  text='Next step',
                     highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE)
reset_button = Button(x=780, y=750, w=200, h=100, text='Reset',
                      highlighted_color=PINK, regular_color=RED)
text_up = Button(x=720, y=580, w=20, h=30, text='^', active_func=text_chat.can_go_up,
                 highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE)
text_down = Button(x=720, y=960, w=20, h=30, text='v', active_func=text_chat.can_go_down,
                   highlighted_color=LIGHT_BLUE, regular_color=NAVY_BLUE)
all_buttons = [step_button, reset_button, text_up, text_down]

# Define the controller and the view instances
controller = Controller(text_chat, game, reset_button, step_button, text_up, text_down)
view = View(pygame)

# Main game loop
while True:
    mouse = pygame.mouse.get_pos()

    # Check for key/mouse events, and handle them
    for event in pygame.event.get():
        controller.handle_event(event, mouse, pygame)

    # Draw the game-screen
    view.draw_game(pygame, screen, game, all_buttons, mouse)
