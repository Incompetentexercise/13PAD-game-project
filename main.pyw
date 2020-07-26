import pygame as pygame
import random as random
import menus
import asteroids


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


class Game:
    def __init__(self):
        # self.state = 'paused'
        self.background_image = pygame.image.load('images/game_background.png')
        self.surface = pygame.image.load('images/game_background.png')
        self.asteroids = []

    def update(self):
        self.surface.blit(self.background_image, self.background_image.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    # the player has paused the game. Enter pause menu
                    menu.game_state = 'in menu'
                    menu.state = 'paused'

        if random.randint(0, 50) == 1:
            self.asteroids.append(asteroids.Asteroid(resolution))

        for asteroid in self.asteroids:
            if asteroid.update(): # if the asteroid is still on the screen
                asteroid.blit(self.surface) # draw the asteroid
            else:
                self.asteroids.remove(asteroid) # asteroid is off the bottom, delete

        # update player
        # draw player


    def blit(self, surface):
        surface.blit(self.surface, self.surface.get_rect())

    def reset(self):
        pass


if __name__ == '__main__':
    pygame.font.init()
    resolution = (450, 600)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    # game_state = 'in menu'

    menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = menus.Menu((resolution[0] / 4, resolution[1] / 8))

    game = Game()
    game.blit(screen)
    pygame.display.update()

    while True:
        clock.tick(30)

        if menu.game_state == 'in menu':
            menu.update()
            menu.blit(screen)
            pygame.display.update(menu.rect)

        elif menu.game_state == "in game":
            game.update()
            game.blit(screen)
            pygame.display.update()
