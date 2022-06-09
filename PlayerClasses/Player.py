import random
from Message import MessageType, Message


class Player:
    def __init__(self, name, role, roles, player_id):
        self.name = name
        self.role = role
        self.alive = True
        self.roles = roles
        self.voted = False
        self.id = player_id
        self.alive_player_ids = list(range(sum(roles.values())))

    def get_vote(self):
        targets = [idx for idx in self.alive_player_ids if idx != self.id]
        return random.choice(targets)

    def inform(self, message):
        if message.message_type == MessageType.DEATH_REPORT:
            self.alive_player_ids.remove(message.players[0])

    def draw(self, pygame, screen, x, y, color, text_color, player_images):
        text_font = pygame.font.SysFont('Corbel', 35)
        if self.alive and not self.voted:
            pygame.draw.rect(screen, (0, 0, 0), [x - 5, y - 5, 210, 260])
        elif self.alive and self.voted:
            pygame.draw.rect(screen, (50, 196, 50), [x - 5, y - 5, 210, 260])
        else:
            pygame.draw.rect(screen, (255, 0, 0), [x - 5, y - 5, 210, 260])
        pygame.draw.rect(screen, color, [x, y, 200, 250])
        text = text_font.render(self.name, True, text_color)
        text_width = text.get_rect().width
        text_height = text.get_rect().height
        screen.blit(text, (x + 100 - text_width // 2, y + 225 - text_height // 2))
        screen.blit(player_images[self.role], (x, y))
        if not self.alive:
            screen.blit(player_images['dead_cross'], (x, y))
