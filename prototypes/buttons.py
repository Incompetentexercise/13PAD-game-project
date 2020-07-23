import pygame as pygame
import sys as sys


class Button:
    def __init__(self, image_directory, position, command):
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

    def update(self):
        """
        Update the buttons state based on the position of the cursor and whether the LMB is pressed
        Calls the button function when button is released
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()): # is the mouse over the button?
            if pygame.mouse.get_pressed()[0]: # is the LMB held down?
                self.state = 'pressed'
            else:
                if self.state == 'pressed':
                    # LMB was pressed and now is released. Execute command
                    self.command()
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


def demo():
    print('button used')


def stop():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init() #Start Pygame
    screen = pygame.display.set_mode((300, 600)) #Start the screen
    clock = pygame.time.Clock()
    mouse_released = None
    buttons = [
        Button('images/play_button', (150, 100), demo),
        Button('images/instructions_button', (150, 240), demo),
        Button('images/power_button', (150, 380), stop),
        Button('images/back_button', (150, 500), demo)
    ]

    while True:
        clock.tick(60)
        screen.fill((230, 230, 230))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #The user closed the window!
                stop() #Close the window

        for button in buttons:
            button.update()
            button.blit(screen)
        pygame.display.update()
