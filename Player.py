from enum import Enum
import random


class Role(Enum):
    WOLF = 1
    VILLAGER = 2
    SEER = 3
    LITTLE_GIRL = 4


class Player:
    def __init__(self, name, role, roles):
        self.name = name
        self.role = role
        self.alive = random.choice([True, False])

    def get_vote(self):
        pass

    def die(self):
        self.alive = False

    def is_alive(self):
        return self.alive

    def draw(self, pygame, screen, location, color, text_font, text_color, player_images):
        pygame.draw.rect(screen, (0, 0, 0), [location[0] - 5, location[1] - 5, 210, 260])
        pygame.draw.rect(screen, color, [*location, 200, 250])
        text = text_font.render(self.name, True, text_color)
        text_width = text.get_rect().width
        text_height = text.get_rect().height
        screen.blit(text, (location[0] + 100 - text_width // 2, location[1] + 225 - text_height // 2))
        screen.blit(player_images[self.role], location)
        if not self.alive:
            screen.blit(player_images['dead_cross'], location)

