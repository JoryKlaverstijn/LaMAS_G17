from Colors import *
from PlayerClasses.Roles import Role
from Game import State


class View:
    def __init__(self, pygame):
        # Load some images for the different player roles
        self.player_images = {
            Role.WOLF: pygame.image.load('Images/wolf_card.jpg'),
            Role.VILLAGER: pygame.image.load('Images/villager_card.jpg'),
            Role.SEER: pygame.image.load('Images/seer_card.jpg'),
            Role.LITTLE_GIRL: pygame.image.load('Images/littlegirl_card.jpg'),
            'dead_cross': pygame.image.load('Images/dead_cross.png').convert_alpha()
        }

    def draw_game(self, pygame, screen, game, all_buttons, mouse):
        """
        Calls all the drawing methods of everything that needs to be drawn in the game.
        """
        # Where to display the player images
        player_locations = [(x, y) for y in (20, 300) for x in range(50, 750, 220)]

        # Drawing background
        screen.fill((50, 50, 50))

        # Drawing players
        for player, location in zip(game.players, player_locations):
            player.draw(pygame, screen, *location, CORAL_RED, BLACK, self.player_images)

        # Drawing in-game text chat
        game.text_chat.draw(pygame, screen)

        # Drawing buttons
        for button in all_buttons:
            button.draw_button(pygame, screen, mouse)

        # If a vote is active: draw the voting counts per player and show who has voted
        if game.state in (State.VOTING_DAY, State.VOTING_NIGHT):
            for player, (x, y), votes in zip(game.players, player_locations, game.votes):
                if player.alive:
                    pygame.draw.circle(screen, DARK_RED, (x + 200, y), 25)
                    pygame.draw.circle(screen, PINK, (x+200, y), 20)
                    text_font = pygame.font.SysFont('Corbel', 35)
                    text = text_font.render(str(votes), True, (0, 0, 0))
                    screen.blit(text, (x+190, y-20))

        pygame.display.update()
