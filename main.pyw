import pygame as pygame
import menus
import asteroids


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


if __name__ == '__main__':
    pygame.font.init()
    resolution = (450, 600)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    game_state = 'in menu'

    menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = menus.Menu((resolution[0] / 4, resolution[1] / 8))

    game_surface = pygame.image.load('images/game_background.png')
    # make game object

    screen.blit(game_surface, game_surface.get_rect())
    pygame.display.update()

    while True:
        if game_state == 'in menu':
            menu.do()
            menu.blit(screen)
            pygame.display.update(menu.rect)

        elif game_state == 'in game':
            # game.do()
            # game.blit(screen)
            pygame.display.update()
