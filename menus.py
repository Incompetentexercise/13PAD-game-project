import pygame as pygame


def create_text(text, font, colour, position):
    _text = font.render(text, False, colour)
    _text_rect = _text.get_rect()
    _text_rect.center = position

    return {'surface': _text, 'rect': _text_rect}


def stop():
    pygame.quit()


class Menu:
    def __init__(self, surface, position):
        self.state = 'main'
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.center = position
        self.resolution = surface.get_size()
        self.center = (self.resolution[0]/2, self.resolution[1]/2)
        self.bg_colour = (0, 0, 0)

        self.fonts = {
            'regular': pygame.font.SysFont('Courier New', 15, False, False),
            'heading': pygame.font.SysFont('Courier New', 18, True, False)
        }
        self.text_colour = (240, 240, 240)

        #  Main menu text |
        self.tx_main_heading = create_text(
            'Game!!', self.fonts['heading'], self.text_colour,
            (self.resolution[0]/2, 30)
        )
        self.tx_play = create_text(
            '[ENTER] - PLAY', self.fonts['regular'], self.text_colour,
            self.center)
        self.tx_instructions = create_text(
            '[I] - INSTRUCTIONS', self.fonts['regular'], self.text_colour,
            (self.center[0], self.center[1]+20)
        )

        #  instructions text |
        self.tx_instruct_heading = create_text(
            'Game Instructions', self.fonts['heading'], self.text_colour,
            (self.resolution[0]/2, 30)
        )

    def do(self):
        if self.state == 'main':
            self.do_main_menu()
        elif self.state == 'instructions':
            self.do_instruction_menu()
        elif self.state == 'paused':
            self.do_pause_menu() #TODO allow getting to main menu from pause menu

    def blit(self, surface):
        surface.blit(self.surface, self.rect)

    def do_main_menu(self):
        self.surface.fill(self.bg_colour)
        self.surface.blit(self.tx_main_heading['surface'], self.tx_main_heading['rect'])
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
                elif event.key in [pygame.K_RETURN]:
                    global game_state
                    game_state = 'in game'

    def do_instruction_menu(self):
        self.surface.fill(self.bg_colour)
        self.surface.blit(self.tx_instruct_heading['surface'], self.tx_instruct_heading['rect'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    self.state = 'main'

    def do_pause_menu(self):
        self.surface.fill(self.bg_colour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    global game_state
                    game_state = 'in game'


if __name__ == '__main__':
    pygame.font.init()
    resolution = (300, 240)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    game_state = 'in menu'

    # create a surface for the menu to display on
    # rendering on a surface allows the game to stay frozen in the background
    menu_surface = pygame.Surface((220, 180))
    menu_font = pygame.font.SysFont('Courier New', 15, False, False)
    menu = Menu(menu_surface, (resolution[0]/2, resolution[1]/2))

    screen.fill((200, 200, 200))
    pygame.display.update()

    while True:
        clock.tick(30)
        if game_state == 'in menu':
            menu.do()
            menu.blit(screen)
            pygame.display.update(menu.rect)

        elif game_state == 'in game':
            screen.fill((200, 200, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  #The user closed the window!
                    stop()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE]:
                        game_state = 'in menu'
                        menu.state = 'paused'

            pygame.display.update()
