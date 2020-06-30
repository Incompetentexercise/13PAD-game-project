import pygame as pygame
from sys import exit


def create_text(text, font, colour, position):
    """
    Takes text(limited unicode), font(pygame font object), colour(RGB tuple), position(x,y tuple)
    Returns a surface with text on it, and a rect for that surface.
    Returns in dict with keys 'surface' and 'rect'
    Render using surface.blit(surface, blit)
    """
    _text = font.render(text, False, colour)
    _text_rect = _text.get_rect()
    _text_rect.center = position # place text centered on given position

    return {'surface': _text, 'rect': _text_rect}


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


class Menu:
    def __init__(self, surface, position):
        """
        Creates and manages a menu window on top of the rest of the game
        This needs a surface to render onto. Minimum recommended size (220, 180)
        The window will be placed centered on the position given
        Has three primary states: Main menu 'main', instruction screen 'instructions', paused menu 'paused'
        State can be changed with menu.state variable

        Each cycle:
        Call menu.do()
          - to update and draw the menu onto its own surface
        Call menu.blit(surface)
          - to draw the menu onto its parent surface or the main screen
        Call pygame.screen.update(menu.rect)
          - if only wanting to update the menu. Leaves the rest of the screen frozen.
            call pygame.screen.update() if wanting to update entire screen
        """

        self.state = 'main' # stores the state of the menu, this is used to choose which menu to render
        self.surface = surface # surface to draw all menu object on to
        self.rect = self.surface.get_rect() # dimensions of the surface
        self.resolution = surface.get_size() # tuple of width and height of surface
        self.rect.center = position # place the surface onto the specified location
        self.center = (self.resolution[0]/2, self.resolution[1]/2) # center for object placement reference
        self.bg_colour = (0, 0, 0) # background colour for the menu surface
        # fonts for use in menus
        self.fonts = {
            # font name, size(pt), bold, italic
            'regular': pygame.font.SysFont('Courier New', 15, False, False),
            'heading': pygame.font.SysFont('Courier New', 18, True, False)
        }
        self.text_colour = (240, 240, 240) # colour for all text in menus

        #  Main menu text |
        self.tx_main_heading = create_text(
            'GAME!!', self.fonts['heading'], self.text_colour,
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
            'INSTRUCTIONS', self.fonts['heading'], self.text_colour,
            (self.resolution[0]/2, 30)
        )
        self.tx_instruct_exit = create_text(
            '[ESC] - BACK', self.fonts['regular'], self.text_colour,
            (self.center[0], self.resolution[1]-30)
        )

        # pause menu text |
        self.tx_paused_heading = create_text(
            'PAUSED', self.fonts['heading'], self.text_colour,
            (self.center[0], 30)
        )
        self.tx_paused_resume = create_text(
            '[ESC] - RESUME', self.fonts['regular'], self.text_colour,
            (self.center[0], 60)
        )
        self.tx_paused_exit = create_text(
            '[M] - EXIT TO MENU', self.fonts['regular'], self.text_colour,
            (self.center[0], self.resolution[1]-30)
        )

    def do(self):
        """
        Looks at the menu state and calls the appropriate method to update and render that menu
        """
        if self.state == 'main':
            self.__do_main_menu()
        elif self.state == 'instructions':
            self.__do_instruction_menu()
        elif self.state == 'paused':
            self.__do_pause_menu() #TODO allow getting to main menu from pause menu

    def blit(self, surface):
        """
        Blits the entire menu onto another surface
        """
        surface.blit(self.surface, self.rect)

    def __do_main_menu(self):
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

    def __do_instruction_menu(self):
        self.surface.fill(self.bg_colour)
        self.surface.blit(self.tx_instruct_heading['surface'], self.tx_instruct_heading['rect'])
        self.surface.blit(self.tx_instruct_exit['surface'], self.tx_instruct_exit['rect'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    self.state = 'main'

    def __do_pause_menu(self):
        self.surface.fill(self.bg_colour)
        self.surface.blit(self.tx_paused_heading['surface'], self.tx_paused_heading['rect'])
        self.surface.blit(self.tx_paused_resume['surface'], self.tx_paused_resume['rect'])
        self.surface.blit(self.tx_paused_exit['surface'], self.tx_paused_exit['rect'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    global game_state
                    game_state = 'in game'
                elif event.key in [pygame.K_m]:
                    self.state = 'main'


if __name__ == '__main__':
    pygame.font.init() # initialise the pygame font module to allow text rendering
    resolution = (300, 240) # resolution of main window
    screen = pygame.display.set_mode(resolution) # create window
    clock = pygame.time.Clock() # create clock object to keep frames on time
    game_state = 'in menu' # keep track of whether game is in menu or playing

    # create a surface for the menu to display on
    # rendering on a surface allows the game to stay frozen in the background
    menu_surface = pygame.Surface((220, 180))
    menu = Menu(menu_surface, (resolution[0]/2, resolution[1]/2))

    # give main screen a background to demonstrate menu above
    screen.fill((200, 200, 200))
    pygame.display.update()

    while True:
        clock.tick(30) # aim for 30 ticks per second
        if game_state == 'in menu': # if in a menu
            menu.do() # update and draw menu
            menu.blit(screen) # blit menu onto screen
            pygame.display.update(menu.rect) # update only the menu

        elif game_state == 'in game':
            screen.fill((200, 200, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  #The user closed the window!
                    stop()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE]:
                        # the player has paused the game. Enter pause menu
                        game_state = 'in menu'
                        menu.state = 'paused'

            pygame.display.update() # update entire screen
