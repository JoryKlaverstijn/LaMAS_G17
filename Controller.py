class Controller:
    """
    The main controller of the game. This class handles button/mouse events.
    It has a close coupling with the Game/model.
    """
    def __init__(self, text_chat, game, reset_button, step_button, text_up, text_down):
        self.text_chat = text_chat
        self.game = game
        self.reset_button = reset_button
        self.step_button = step_button
        self.text_up = text_up
        self.text_down = text_down

    def handle_event(self, event, mouse, pygame):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit()

        # Handle mouse clicks (all clickable buttons)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.step_button.mouse_on_button(mouse):
                winner = self.game.game_over()
                if winner:
                    self.text_chat.add_message(f"Game Over, {winner} have won!", (96, 255, 96))
                else:
                    self.game.step()

            if self.reset_button.mouse_on_button(mouse):
                self.game.reset()

            if self.text_up.mouse_on_button(mouse) and self.text_chat.can_go_up():
                self.text_chat.cursor -= 1

            if self.text_down.mouse_on_button(mouse) and self.text_chat.can_go_down():
                self.text_chat.cursor += 1

        # Handle buttons (Space, up, down)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.text_chat.can_go_up():
                self.text_chat.cursor -= 1

            if event.key == pygame.K_DOWN and self.text_chat.can_go_down():
                self.text_chat.cursor += 1

            if event.key == pygame.K_SPACE:
                winner = self.game.game_over()
                if winner:
                    self.text_chat.add_message(f"Game Over, {winner} have won!", (96, 255, 96))
                else:
                    self.game.step()

            if event.key == pygame.K_BACKSPACE:
                self.game.reset()
