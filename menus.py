import pygame as pygame


def create_text(text, font, colour, position):
    _text = font.render(text, False, colour)
    _text_rect = _text.get_rect()
    _text_rect.center = position

    return {'surface': _text, 'rect': _text_rect}


class Menu:
    def __init__(self, screen, font, resolution):
        self.state = 'main'
        self.screen = screen
        self.font = font
        self.text_colour = (240, 240, 240)
        self.resolution = resolution
        self.center = (resolution[0]/2, resolution[1]/2)

        self.tx_play = self.font.render('[ENTER] - Play', False, self.text_colour)
        self.tx_play_rect = self.tx_play.get_rect()
        self.tx_play_rect.center = self.center

        self.tx_instructions = self.font.render('[I] - Instructions', False, self.text_colour)
        self.tx_instruction_rect = self.tx_instructions.get_rect()
        self.tx_instruction_rect.center = (self.center[0], self.center[1]+20)

    def do(self):
        if self.state == 'main':
            self.do_main_menu()
        elif self.state == 'instructions':
            self.do_instruction_menu()

    def do_main_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.tx_play, self.tx_play_rect)
        self.screen.blit(self.tx_instructions, self.tx_instruction_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                pygame.quit()  #Close the window
                running = False

    def do_instruction_menu(self):
        pass


if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    menu_font = pygame.font.SysFont('Courier New', 15, False, False)

    menu = Menu(screen, menu_font, (640, 480))
    while True:
        clock.tick(30)
        menu.do()
        pygame.display.update()
