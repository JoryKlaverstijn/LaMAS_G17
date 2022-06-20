class Button:
    def __init__(self, x, y, w, h, text, highlighted_color, regular_color):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text = text
        self.color1 = highlighted_color
        self.color2 = regular_color

    def mouse_on_button(self, mouse):
        return (self.x < mouse[0] < (self.x + self.w)) and (self.y < mouse[1] < self.y + self.h)

    def draw_button(self, pygame, screen, selected):
        pygame.draw.rect(screen, (0, 0, 0), [self.x-5, self.y-5, self.w+10, self.h+10])
        if selected:
            pygame.draw.rect(screen, self.color1, [self.x, self.y, self.w, self.h])
        else:
            pygame.draw.rect(screen, self.color2, [self.x, self.y, self.w, self.h])

        text_width = self.text.get_rect().width
        text_height = self.text.get_rect().height
        screen.blit(self.text, (self.x + self.w // 2 - text_width // 2, self.y + self.h // 2 - text_height // 2))





