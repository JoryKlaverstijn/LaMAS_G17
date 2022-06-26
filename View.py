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
            Role.HUNTER: pygame.image.load('Images/hunter_card.jpg'),
            'dead_cross': pygame.image.load('Images/dead_cross.png').convert_alpha()
        }
        self.bg_image = pygame.image.load('Images/background.png')

    def draw_player(self, pygame, screen, location, color, text_color, player):
        text_font = pygame.font.SysFont('Corbel', 35)
        # Draw the player card and the border of the player card
        if player.voted:
            pygame.draw.rect(screen, (255, 0, 255), [location[0] - 5, location[1] - 5, 210, 260])
        else:
            pygame.draw.rect(screen, (0, 0, 0), [location[0] - 5, location[1] - 5, 210, 260])
        pygame.draw.rect(screen, color, [*location, 200, 250])

        # Draw the name of the player
        text = text_font.render(player.name, True, text_color)
        text_width = text.get_rect().width
        text_height = text.get_rect().height
        screen.blit(text, (location[0] + 100 - text_width // 2, location[1] + 225 - text_height // 2))

        # Draw the player image, and if the player has died, a cross
        screen.blit(self.player_images[player.role], location)
        if not player.alive:
            screen.blit(self.player_images['dead_cross'], location)

        # Draw the player number
        pygame.draw.rect(screen, (0, 0, 0), [location[0] - 5, location[1] - 5, 45, 45])
        pygame.draw.rect(screen, NAVY_BLUE, [location[0], location[1], 35, 35])
        text = text_font.render(str(player.id + 1), True,  (255, 255, 255))
        screen.blit(text, location)

    def draw_game(self, pygame, screen, game, all_buttons, mouse):
        """
        Calls all the drawing methods of everything that needs to be drawn in the game.
        """
        # Where to display the player images
        player_locations = [(x, y) for y in (20, 300) for x in range(50, 750, 220)]

        # Drawing background
        screen.blit(self.bg_image, (0, 0))

        # Drawing players
        for player, location in zip(game.players, player_locations):
            self.draw_player(pygame, screen, location, CORAL_RED, BLACK, player)

        # Drawing in-game text chat
        game.text_chat.draw(pygame, screen)

        # Drawing buttons
        for button in all_buttons:
            button.draw_button(pygame, screen, mouse)

        # If a vote is active: draw the voting counts per player and show who has voted
        if game.state in (State.VOTING_DAY, State.VOTING_NIGHT, State.VOTING_DAY_RESULTS, State.VOTING_NIGHT_RESULTS):
            for player, (x, y), votes in zip(game.players, player_locations, game.votes):
                if player.alive:
                    pygame.draw.circle(screen, DARK_RED, (x + 200, y), 25)
                    pygame.draw.circle(screen, PINK, (x+200, y), 20)
                    text_font = pygame.font.SysFont('Corbel', 35)
                    text = text_font.render(str(votes), True, (0, 0, 0))
                    screen.blit(text, (x+190, y-20))

        pygame.display.update()
