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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            'forward': {
                'slow': pygame.image.load("images/player/forward_slow.png").convert_alpha(),
                'fast': pygame.image.load("images/player/forward_fast.png").convert_alpha()
            },
            'left': {
                'slow': pygame.image.load("images/player/left_slow.png").convert_alpha(),
                'fast': pygame.image.load("images/player/left_fast.png").convert_alpha()
            },
            'right': {
                'slow': pygame.image.load("images/player/right_slow.png").convert_alpha(),
                'fast': pygame.image.load("images/player/right_fast.png").convert_alpha()
            }
        }
        self.direction = 'forward'
        self.speed = 'slow'
        self.horizontal_speed = 5
        self.position = [resolution[0]/2, resolution[1]-50]
        self.surface = None
        self.rect = None
        self.pressed_keys = None
        self.left_pressed = None
        self.right_pressed = None

    def update(self, speed_multiplier):
        self.pressed_keys = pygame.key.get_pressed() # get a list of all the keys that are currently pressed
        if self.pressed_keys[pygame.K_LEFT] or self.pressed_keys[pygame.K_a]:
            self.left_pressed = True
        else:
            self.left_pressed = False

        if self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[pygame.K_d]:
            self.right_pressed = True
        else:
            self.right_pressed = False

        # update player direction
        if self.left_pressed and self.right_pressed:
            self.direction = 'forward'
        elif self.left_pressed:
            self.direction = 'left'
        elif self.right_pressed:
            self.direction = 'right'
        else:
            self.direction = 'forward'

        if speed_multiplier > 1:
            self.speed = 'fast'
        else:
            self.speed = 'slow'
        self.surface = self.images[self.direction][self.speed]
        if self.direction == 'left':
            if self.position[0] >= 0:
                self.position[0] -= self.horizontal_speed*speed_multiplier
        elif self.direction == 'right':
            if self.position[0] <= resolution[0]:
                self.position[0] += self.horizontal_speed*speed_multiplier

        self.rect = self.surface.get_rect(center=self.position)

    def blit(self, surface):
        surface.blit(self.surface, self.rect)


class Game:
    def __init__(self):
        # self.state = 'paused'
        self.background_image = pygame.image.load('images/game_background.png')
        self.surface = pygame.image.load('images/game_background.png')
        self.asteroids = []
        self.player = Player()
        # self.player_direction = 'forward'
        self.speed_multiplier = 1
        self.pressed_keys = None
        self.up_pressed = None

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

        self.pressed_keys = pygame.key.get_pressed()

        if self.pressed_keys[pygame.K_UP] or self.pressed_keys[pygame.K_w] or self.pressed_keys[pygame.KMOD_SHIFT]:
            self.up_pressed = True
        else:
            self.up_pressed = False

        if self.up_pressed:
            self.speed_multiplier = 1.8
        else:
            self.speed_multiplier = 1

        if random.randint(0, 15) == 1:
            self.asteroids.append(asteroids.Asteroid(resolution))

        for asteroid in self.asteroids:
            if asteroid.update(self.speed_multiplier): # if the asteroid is still on the screen
                asteroid.blit(self.surface) # draw the asteroid
            else:
                self.asteroids.remove(asteroid) # asteroid is off the bottom, delete

        self.player.update(self.speed_multiplier)
        self.player.blit(self.surface)

    def blit(self, surface):
        surface.blit(self.surface, self.surface.get_rect())

    def reset(self):
        pass


if __name__ == '__main__':
    pygame.font.init()
    resolution = (450, 600)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = menus.Menu((resolution[0] / 3.4, resolution[1] / 8))

    game = Game()
    game.blit(screen)
    pygame.display.update()

    while True:
        clock.tick(60) # keep framerate at 60fps

        if menu.game_state == 'in menu':
            menu.update()
            menu.blit(screen)
            pygame.display.update(menu.rect)

        elif menu.game_state == "in game":
            game.update()
            game.blit(screen)
            pygame.display.update()
