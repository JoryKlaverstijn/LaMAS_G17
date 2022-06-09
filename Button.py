class Button:
    def __init__(self, x, y, w, h, text, highlighted_color, regular_color, active_func=None):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text = text
        self.color1 = highlighted_color
        self.color2 = regular_color
        self.active_func = active_func  # A function passed that is called to check if the button is inactive (drawing)

    def mouse_on_button(self, mouse):
        """
        Checks if the mouse location is in the area of the button.
        """
        return (self.x < mouse[0] < (self.x + self.w)) and (self.y < mouse[1] < self.y + self.h)

    def draw_button(self, pygame, screen, mouse):
        """
        Draws the button with the color based on whether or not the mouse is on the button.
        """
        text_font = pygame.font.SysFont('Corbel', 35)
        rendered_text = text_font.render(self.text, True, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), [self.x-5, self.y-5, self.w+10, self.h+10])
        if self.active_func is not None and not self.active_func():
            pygame.draw.rect(screen, (255, 255, 255), [self.x, self.y, self.w, self.h])
        elif self.mouse_on_button(mouse):
            pygame.draw.rect(screen, self.color1, [self.x, self.y, self.w, self.h])
        else:
            pygame.draw.rect(screen, self.color2, [self.x, self.y, self.w, self.h])

        text_width = rendered_text.get_rect().width
        text_height = rendered_text.get_rect().height
        screen.blit(rendered_text, (self.x + self.w // 2 - text_width // 2, self.y + self.h // 2 - text_height // 2))
