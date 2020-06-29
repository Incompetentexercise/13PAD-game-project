import pygame as pygame


def create_text(text, font, colour, position):
    _text = font.render(text, False, colour)
    _text_rect = _text.get_rect()
    _text_rect.center = position

    return {'surface': _text, 'rect': _text_rect}


def stop():
    pygame.quit()


class Menu:
    def __init__(self, surface, font, position):
        self.state = 'main'
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.center = position
        self.font = font
        self.text_colour = (240, 240, 240)
        self.resolution = surface.get_size()

        self.center = (self.resolution[0]/2, self.resolution[1]/2)

        self.tx_play = create_text('[ENTER] - PLAY', self.font, self.text_colour, self.center)
        self.tx_instructions = create_text(
            '[I] - INSTRUCTIONS', self.font, self.text_colour,
            (self.center[0], self.center[1]+20)
        )

    def do(self):
        if self.state == 'main':
            self.do_main_menu()
        elif self.state == 'instructions':
            self.do_instruction_menu()

    def blit(self, surface):
        surface.blit(self.surface, self.rect)

    def do_main_menu(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.tx_play['surface'], self.tx_play['rect'])
        self.surface.blit(self.tx_instructions['surface'], self.tx_instructions['rect'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    stop()
                elif event.key in [pygame.K_i]:
                    self.state = 'instructions'

    def do_instruction_menu(self):
        self.surface.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    self.state = 'main'


if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    game_state = 'in menu'

    menu_surface = pygame.Surface((200, 250))
    menu_font = pygame.font.SysFont('Courier New', 15, False, False)
    menu = Menu(menu_surface, menu_font, (320, 240))

    screen.fill((50, 50, 50))
    pygame.display.update()

    while True:
        clock.tick(30)
        if game_state == 'in menu':
            menu.do()
            menu.blit(screen)
            pygame.display.update(menu.rect)
