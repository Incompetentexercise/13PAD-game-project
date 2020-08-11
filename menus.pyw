import pygame as pygame
from sys import exit

ButtonPress = pygame.USEREVENT+1
GameCommand = pygame.USEREVENT+2
button_events = {
    'PLAY': pygame.event.Event(ButtonPress, {'name': 'PLAY'}),
    'INSTRUCTIONS': pygame.event.Event(ButtonPress, {'name': 'INSTRUCTIONS'}),
    'INTERNAL_EXIT': pygame.event.Event(ButtonPress, {'name': 'INTERNAL_EXIT'})
}
game_events = {
    'RESTART': pygame.event.Event(GameCommand, {'command': 'RESTART'})
}


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


def blit_text(text_list, surface):
    for text_obj in text_list:
        surface.blit(text_obj['surface'], text_obj['rect'])


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


class Button:
    def __init__(self, image_directory, position, parent_position, event):
        """
        Creates, updates, and draws buttons
        Takes:
            image directory - this is a folder with images for each state
                The images be named 'idle.png' 'hover.png' 'pressed.png'
            position - a tuple (x, y) position in pixels. button will be centered
            command - the function/method to call when the button is pressed
                should be given as a tuple of (command, argument)
                if there is no argument then pass (command, None)
                make sure to pass the command without brackets eg: self.example, not self.example()

        Each button has three states:
            idle
            hover - when the cursor is over the top
            pressed - when the left mouse button is pressed over the button

        Each tick:
            Call .update() followed by .blit(surface) for each button.
        """

        # load the images for each button state
        # .convert_alpha allows transparency
        self.images = {
            "idle": pygame.image.load(image_directory + "/idle.png").convert_alpha(),
            "hover": pygame.image.load(image_directory + "/hover.png").convert_alpha(),
            "pressed": pygame.image.load(image_directory + "/pressed.png").convert_alpha()
        }

        self.event = event
        self.state = 'idle'
        self.position = position
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()
        self.parent_position = parent_position
        self.mouse_pos = None
        self.absolute_position = (parent_position[0]+self.position[0], parent_position[1], self.position[1])

    def update(self):
        """
        Update the buttons state based on the position of the cursor and whether the LMB is pressed
        Calls the button function when button is released
        """

        # get the mouse position. make the mouse 0 position the menu 0 position.
        # not doing this stops the collision detection working
        self.mouse_pos = (
            pygame.mouse.get_pos()[0] - self.parent_position[0], # mouse x pos
            pygame.mouse.get_pos()[1] - self.parent_position[1] # mouse y pos
        )
        if self.rect.collidepoint(self.mouse_pos): # is the mouse over the button?
            if pygame.mouse.get_pressed()[0]: # is the LMB held down?
                self.state = 'pressed'
            else:
                if self.state == 'pressed':
                    # LMB was pressed and now is released. Execute linked command
                    pygame.event.post(self.event)
                self.state = 'hover' # LMB has been released. show button not pressed
        else:
            self.state = 'idle' # the button is not being interacted with

        # update the image and position to match the state
        self.image = self.images[self.state]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def blit(self, surface):
        """ Draw the button onto the given surface. """
        surface.blit(self.image, self.rect)


class Menu:
    def __init__(self, position):
        """
        Creates and manages a menu window on top of the rest of the game
        This needs a surface to render onto. Minimum recommended size (220, 180)
        The top left corner of the window will be placed at the given location
        Has three primary states: Main menu 'main', instruction screen 'instructions', paused menu 'paused'
        State can be changed with menu.state variable

        Each tick:
        Call menu.update()
          - to update and draw the menu onto its own surface
        Call menu.blit(surface)
          - to draw the menu onto a surface or the main screen
        Call pygame.screen.update(menu.rect)
          - if only wanting to update the menu. Leaves the rest of the screen frozen.
            call pygame.screen.update() if wanting to update entire screen
        """

        self.game_state = 'in menu'
        self.state = 'main' # stores the state of the menu, this is used to choose which menu to render

        # store the background images so the screen can be cleared each tick
        self.large_background_image = pygame.image.load('images/large_menu_background.png').convert_alpha()
        self.wide_background_image = pygame.image.load('images/instructions_background.png').convert_alpha()
        self.small_background_image = pygame.image.load('images/small_menu_background.png').convert_alpha()

        # make a surface from the given image. all the menu elements will be drawn on this surface
        self.surface = self.large_background_image.copy()
        self.rect = self.surface.get_rect()
        self.resolution = self.surface.get_size()

        self.position = position # store given position
        # place the surface onto the specified position
        self.rect.left = position[0]
        self.rect.top = position[1]
        self.center = (self.resolution[0]/2, self.resolution[1]/2) # center of surface for object placement reference

        # fonts for use in menus
        self.fonts = {
            # font name, size(pt), bold, italic
            'regular': pygame.font.SysFont('Courier New', 15, False, False),
            'heading': pygame.font.SysFont('Courier New', 18, True, False)
        }
        self.text_colour = (255, 255, 255) # colour for all text in menus

        #  Main menu objects |
        self.main_menu_text = []
        self.main_menu_buttons = [
            Button('images/play_button', (self.center[0], 90), self.position, button_events['PLAY']),
            Button('images/instructions_button', (self.center[0], 240), self.position, button_events['INSTRUCTIONS']),
            Button('images/power_button', (self.center[0], 390), self.position, pygame.QUIT)
        ]

        # Instruction menu objects
        self.instruction_menu_text = [
            create_text(
                'INSTRUCTIONS', self.fonts['heading'], self.text_colour,
                (self.resolution[0] / 2, 30)
            )
        ]
        self.instruction_menu_buttons = [
            Button('images/back_button', (self.center[0], 420), self.position, button_events['INTERNAL_EXIT'])
        ]
        self.instructions_image = pygame.image.load("images/instructions.png").convert_alpha()

        # pause menu objects |
        self.paused_menu_text = [
            create_text(
                'PAUSED', self.fonts['heading'], self.text_colour,
                (self.center[0], 30)
            )
        ]
        self.pause_menu_buttons = [
            Button('images/internal_exit_button', (self.center[0], 200), self.position, button_events['INTERNAL_EXIT']),
            Button('images/internal_forward_button', (self.center[0], 100), self.position, button_events['PLAY'])
        ]

        # death menu objects
        self.death_menu_text = [
            create_text(
                'YOU CRASHED', self.fonts['heading'], self.text_colour,
                (self.center[0], 40)
            )
        ]
        self.death_menu_buttons = [
            Button('images/internal_forward_button', (self.center[0], 100), self.position, button_events['PLAY']),
            Button('images/internal_exit_button', (self.center[0], 200), self.position, button_events['INTERNAL_EXIT']),
        ]

    def update(self):
        """
        Looks at the menu state and calls the appropriate method to update and render that menu
        """

        # does this menu need a big or small background?
        if self.state in ['main']:
            self.surface = self.large_background_image.copy()
            self.rect = self.surface.get_rect()
            self.surface.blit(self.large_background_image, self.rect)

        elif self.state in ['instructions']:
            self.surface = self.wide_background_image.copy()
            self.rect = self.surface.get_rect()
            self.surface.blit(self.wide_background_image, self.rect)

        elif self.state in ['paused', 'death']:
            self.surface = self.small_background_image.copy()
            self.rect = self.surface.get_rect()
            self.surface.blit(self.small_background_image, self.rect)

        self.resolution = self.surface.get_size()
        # place surface in correct position
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

        if self.state == 'main':
            self.__do_main_menu()
        elif self.state == 'instructions':
            self.__do_instruction_menu()
        elif self.state == 'paused':
            self.__do_pause_menu()
        elif self.state == 'death':
            self.__do_death_menu()

    def blit(self, surface):
        """
        Blits the entire menu onto another surface
        """
        surface.blit(self.surface, self.rect)

    def __do_main_menu(self):
        blit_text(self.main_menu_text, self.surface)
        for button in self.main_menu_buttons:
            button.update()
            button.blit(self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

            if event.type == ButtonPress:
                if event.name == 'PLAY':
                    self.game_state = 'in game'
                    pygame.event.post(game_events['RESTART'])
                elif event.name == 'INSTRUCTIONS':
                    self.state = 'instructions'

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    stop()
                elif event.key in [pygame.K_i]:
                    self.state = 'instructions'
                elif event.key in [pygame.K_RETURN]:
                    self.game_state = 'in game'

    def __do_instruction_menu(self):
        blit_text(self.instruction_menu_text, self.surface)
        self.surface.blit(self.instructions_image, self.instructions_image.get_rect())

        for button in self.instruction_menu_buttons:
            button.update()
            button.blit(self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

            if event.type == ButtonPress:
                if event.name == 'INTERNAL_EXIT':
                    self.state = 'main'

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    self.state = 'main'

    def __do_pause_menu(self):
        blit_text(self.paused_menu_text, self.surface)

        for button in self.pause_menu_buttons:
            button.update()
            button.blit(self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

            if event.type == ButtonPress:
                if event.name == 'INTERNAL_EXIT':
                    self.state = 'main'
                elif event.name == 'PLAY':
                    self.game_state = 'in game'

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    global game_state
                    game_state = 'in game'
                elif event.key in [pygame.K_m]:
                    self.state = 'main'

    def __do_death_menu(self):
        blit_text(self.death_menu_text, self.surface)

        for button in self.death_menu_buttons:
            button.update()
            button.blit(self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

            elif event.type == ButtonPress:
                if event.name == 'INTERNAL_EXIT':
                    self.state = 'main'
                elif event.name == 'PLAY':
                    self.game_state = 'in game'
                    pygame.event.post(game_events['RESTART'])


if __name__ == '__main__':
    pygame.font.init() # initialise the pygame font module to allow text rendering
    resolution = (450, 600) # resolution of main window
    screen = pygame.display.set_mode(resolution) # create window
    clock = pygame.time.Clock() # create clock object to keep frames on time
    # game_state = 'in menu' # keep track of whether game is in menu or playing

    # create a surface for the menu to display on
    # rendering on a surface allows the game to stay frozen in the background
    # menu_surface = pygame.Surface((200, 500))
    # menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = Menu((resolution[0]/4, resolution[1]/8))

    # give main screen a background to demonstrate menus above
    screen.fill((0, 0, 0))
    pygame.display.update()

    while True:
        clock.tick(30) # aim for 30 ticks per second
        if menu.game_state == 'in menu': # if in a menu
            menu.update() # update and draw menu
            menu.blit(screen) # blit menu onto screen
            pygame.display.update(menu.rect) # update only the menu

        elif menu.game_state == 'in game':
            screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  #The user closed the window!
                    stop()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE]:
                        # the player has paused the game. Enter pause menu
                        menu.game_state = 'in menu'
                        menu.state = 'paused'

            pygame.display.update() # update entire screen
