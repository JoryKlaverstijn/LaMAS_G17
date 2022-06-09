import numpy as np


class TextChat:
    """
    This is the class for the text chat of the game.
    This chat shows messages by players, but also in-game events, like votes.
    """
    def __init__(self, x, y, w, h, bg_color, max_len=18):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.bg_color = bg_color
        self.max_len = max_len
        self.cursor = 0
        self.messages = []

    def add_message(self, text, color=(255, 255, 255)):
        """
        Adds a colored message to the chat. Scrolls to the bottom of the chat.
        """
        self.messages.append((text, color))
        while self.can_go_down():
            self.cursor += 1

    def can_go_down(self):
        """
        Checks if the chat can be scrolled down.
        """
        return self.cursor + self.max_len < len(self.messages)

    def can_go_up(self):
        """
        Checks if the chat can be scrolled up.
        """
        return self.cursor > 0

    def draw(self, pygame, screen):
        """
        Draws the chat box and all the messages.
        """
        pygame.draw.rect(screen, (0, 0, 0), [self.x-5, self.y-5, self.w+10, self.h+10])
        pygame.draw.rect(screen, self.bg_color, [self.x, self.y, self.w, self.h])
        message_y_coords = np.linspace(self.y, self.y+self.h, self.max_len+2)[:-1]
        chat_font = pygame.font.SysFont('Corbel', 25)
        for (msg, color), y_coord in zip(self.messages[self.cursor:self.cursor+self.max_len], message_y_coords):
            text = chat_font.render('- ' + msg, True, color)
            screen.blit(text, (self.x, int(y_coord)))

        if self.cursor > 0:
            pygame.draw.rect(screen, (128, 128, 196), [self.x, self.y, self.w, 10])

        if self.cursor + self.max_len < len(self.messages):
            pygame.draw.rect(screen, (128, 128, 196), [self.x, self.y+self.h-10, self.w, 10])

    def reset(self):
        """
        Resets the chat. removing any messages from the previous game.
        """
        self.cursor = 0
        self.messages = []
