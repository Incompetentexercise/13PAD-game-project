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
    def __init__(self, image_directory, position, parent_position, command):
        """
        Creates, updates, and draws buttons
        Takes:
            image directory - this is a folder with images for each state
                The images be named 'idle.png' 'hover.png' 'pressed.png'
            position - a tuple (x, y) position in pixels. button will be centered
            command - the function/method to call when the button is pressed
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

        self.command = command
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
        # print("mouse pos", pygame.mouse.get_pos())
        # print("button center", self.rect.center)
        self.mouse_pos = (
            pygame.mouse.get_pos()[0] - self.parent_position[0],
            pygame.mouse.get_pos()[1] - self.parent_position[1]
        )
        if self.rect.collidepoint(self.mouse_pos): # is the mouse over the button?
            if pygame.mouse.get_pressed()[0]: # is the LMB held down?
                self.state = 'pressed'
            else:
                if self.state == 'pressed':
                    # LMB was pressed and now is released. Execute command
                    self.command[0](self.command[1])
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
        The window will be placed centered on the position given
        Has three primary states: Main menu 'main', instruction screen 'instructions', paused menu 'paused'
        State can be changed with menu.state variable

        Each tick:
        Call menu.do()
          - to update and draw the menu onto its own surface
        Call menu.blit(surface)
          - to draw the menu onto a surface or the main screen
        Call pygame.screen.update(menu.rect)
          - if only wanting to update the menu. Leaves the rest of the screen frozen.
            call pygame.screen.update() if wanting to update entire screen
        """

        self.state = 'main' # stores the state of the menu, this is used to choose which menu to render
        self.surface = pygame.image.load('images/menu_background.png').convert_alpha() # surface to draw all menu object on to
        self.background = pygame.image.load('images/menu_background.png').convert_alpha()
        self.rect = self.surface.get_rect() # dimensions of the surface
        self.resolution = self.surface.get_size() # tuple of width and height of surface
        self.position = position
        self.rect.left = position[0] # place the surface onto the specified location
        self.rect.top = position[1]
        self.center = (self.resolution[0]/2, self.resolution[1]/2) # center for object placement reference
        self.bg_colour = (200, 200, 200) # background colour for the menu surface
        # fonts for use in menus
        self.fonts = {
            # font name, size(pt), bold, italic
            'regular': pygame.font.SysFont('Courier New', 15, False, False),
            'heading': pygame.font.SysFont('Courier New', 18, True, False)
        }
        self.text_colour = (30, 30, 30) # colour for all text in menus

        #  Main menu objects |
        self.main_menu_text = [
            create_text(
                'GAME!!', self.fonts['heading'], self.text_colour,
                (self.resolution[0] / 2, 30)
            )
        ]
        self.main_menu_buttons = [
            Button('images/play_button', (self.center[0], 90), self.position, (self.switch_state, "in game")),
            Button('images/instructions_button', (self.center[0], 240), self.position, (self.switch_state, "instructions")),
            Button('images/power_button', (self.center[0], 390), self.position, (stop, None))
        ]

        # Instruction menu objects
        self.instruction_menu_text = [
            create_text(
                'INSTRUCTIONS', self.fonts['heading'], self.text_colour,
                (self.resolution[0] / 2, 30)
            )
        ]
        self.instruction_menu_buttons = [
            Button('images/back_button', (self.center[0], 420), self.position, (self.switch_state, "main"))
        ]

        # pause menu objects |
        self.paused_menu_text = [
            create_text(
                'PAUSED', self.fonts['heading'], self.text_colour,
                (self.center[0], 30)
            )
        ]
        self.pause_menu_buttons = [
            Button('images/internal_exit_button', (self.center[0], 420), self.position, (self.switch_state, "main")),
            Button('images/internal_forward_button', (self.center[0], 100), self.position, (self.switch_state, 'in game'))
        ]

    def do(self):
        """
        Looks at the menu state and calls the appropriate method to update and render that menu
        """
        self.surface.blit(self.background, self.background.get_rect())
        if self.state == 'main':
            self.__do_main_menu()
        elif self.state == 'instructions':
            self.__do_instruction_menu()
        elif self.state == 'paused':
            self.__do_pause_menu()

    def switch_state(self, target_state):
        if target_state == "in game":
            global game_state
            game_state = "in game"
        else:
            self.state = target_state

    def blit(self, surface):
        """
        Blits the entire menu onto another surface
        """
        surface.blit(self.surface, self.rect)

    def __do_main_menu(self):
        blit_text(self.main_menu_text, self.surface)

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

        for button in self.main_menu_buttons:
            button.update()
            button.blit(self.surface)

    def __do_instruction_menu(self):
        blit_text(self.instruction_menu_text, self.surface)
        for button in self.instruction_menu_buttons:
            button.update()
            button.blit(self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    self.state = 'main'

    def __do_pause_menu(self):
        blit_text(self.paused_menu_text, self.surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    global game_state
                    game_state = 'in game'
                elif event.key in [pygame.K_m]:
                    self.state = 'main'

        for button in self.pause_menu_buttons:
            button.update()
            button.blit(self.surface)


if __name__ == '__main__':
    pygame.font.init() # initialise the pygame font module to allow text rendering
    resolution = (600, 700) # resolution of main window
    screen = pygame.display.set_mode(resolution) # create window
    clock = pygame.time.Clock() # create clock object to keep frames on time
    game_state = 'in menu' # keep track of whether game is in menu or playing

    # create a surface for the menu to display on
    # rendering on a surface allows the game to stay frozen in the background
    # menu_surface = pygame.Surface((200, 500))
    menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = Menu((resolution[0]/3, resolution[1]/6))

    # give main screen a background to demonstrate menu above
    screen.fill((240, 240, 240))
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
