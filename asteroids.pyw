import pygame as pygame


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


if __name__ == '__main__':
    pygame.font.init()  # initialise the pygame font module to allow text rendering
    resolution = (450, 600)  # resolution of main window
    screen = pygame.display.set_mode(resolution)  # create window
    clock = pygame.time.Clock()  # create clock object to keep frames on time

    # give main screen a background to demonstrate menus above
    screen.fill((0, 0, 0))
    pygame.display.update()
