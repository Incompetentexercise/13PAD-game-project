import pygame as pygame
import menus
import asteroids
from math import sin, cos, radians

GENERATE_OBSTACLE = pygame.USEREVENT+3


def resolve_velocity(direction, speed):
    if 0 > direction > 180: # bullet would be travelling down, not okay.
        return 'why?'
    elif direction < 90:
        __theta = direction
        __x = -speed*cos(radians(__theta))
    else:
        __theta = 180 - direction
        __x = speed*cos(radians(__theta))
    __y = speed*sin(radians(__theta))

    return __x, __y


def stop():
    """
    Terminate the entire program safely
    """
    pygame.quit() # stop pygame
    exit() # stop python


def check_collisions(primary, secondaries):
    collisions = pygame.sprite.spritecollide(primary, secondaries, False, pygame.sprite.collide_mask)
    return collisions


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        self.position = list(position)
        self.images = [
            pygame.image.load('images/bullets/0.png').convert_alpha(),
            pygame.image.load('images/bullets/1.png').convert_alpha(),
            pygame.image.load('images/bullets/2.png').convert_alpha()
        ]
        self.image_counter = 0
        self.image = self.images[self.image_counter]
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(pygame.image.load('images/bullets/mask.png').convert_alpha())

        self.direction = direction
        self.speed = 25
        self.move_amount = (0, 0)

    def update(self, speed_multiplier):
        self.move_amount = resolve_velocity(self.direction, self.speed/speed_multiplier)
        self.position[0] += self.move_amount[0]
        self.position[1] -= self.move_amount[1]
        self.image_counter += 1
        self.image = self.images[int(self.image_counter/10)]
        if self.image_counter == 29:
            self.image_counter = 0
        self.rect.center = self.position


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
        self.image = None
        self.rect = None
        self.mask = None
        self.pressed_keys = None
        self.left_pressed = None
        self.right_pressed = None
        self.__temp_bullet = None

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
        self.image = self.images[self.direction][self.speed]
        self.mask = pygame.mask.from_surface(self.image)

        if self.direction == 'left':
            if self.position[0] >= 0:
                self.position[0] -= self.horizontal_speed*speed_multiplier
        elif self.direction == 'right':
            if self.position[0] <= resolution[0]:
                self.position[0] += self.horizontal_speed*speed_multiplier

        self.rect = self.image.get_rect(center=self.position)

    def shoot(self):
        if self.direction == 'left':
            self.__temp_bullet = Bullet(self.position, 60)
        elif self.direction == 'forward':
            self.__temp_bullet = Bullet(self.position, 90)
        else:
            self.__temp_bullet = Bullet(self.position, 120)
        global game
        game.sprites.add(self.__temp_bullet)
        game.bullets.add(self.__temp_bullet)


class Game:
    def __init__(self, difficulty):
        # self.state = 'paused'
        self.background_image = pygame.image.load('images/game_background.png')
        self.surface = pygame.image.load('images/game_background.png')
        self.asteroids = pygame.sprite.Group()
        pygame.time.set_timer(GENERATE_OBSTACLE, int(200/difficulty))
        self.sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player()
        self.sprites.add(self.player)

        # self.player_direction = 'forward'
        self.speed_multiplier = 1
        self.speed_multiplier_multiplier = 1 # used to gradually increase the speed
        self.pressed_keys = None
        self.up_pressed = None

    def update(self):
        self.surface.blit(self.background_image, self.background_image.get_rect())
        self.speed_multiplier_multiplier += 0.0002

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    # the player has paused the game. Enter pause menu
                    menu.game_state = 'in menu'
                    menu.state = 'paused'
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()
            elif event.type == GENERATE_OBSTACLE:
                __asteroid = asteroids.Asteroid(resolution)
                self.asteroids.add(__asteroid)
                self.sprites.add(__asteroid)

        self.pressed_keys = pygame.key.get_pressed()

        if self.pressed_keys[pygame.K_UP] or self.pressed_keys[pygame.K_w] or self.pressed_keys[pygame.KMOD_SHIFT]:
            self.up_pressed = True
        else:
            self.up_pressed = False

        if self.up_pressed:
            self.speed_multiplier = 1.8
        else:
            self.speed_multiplier = 1

        self.sprites.update(self.speed_multiplier*self.speed_multiplier_multiplier)
        pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True, pygame.sprite.collide_mask)
        self.sprites.draw(self.surface)
        if check_collisions(self.player, self.asteroids):
            print('collided')
            menu.game_state = 'in menu'
            menu.state = 'death'

    def blit(self, surface):
        surface.blit(self.surface, self.surface.get_rect())


if __name__ == '__main__':
    pygame.font.init()
    resolution = (450, 600)
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    # menu_surface = pygame.image.load('images/menu_background.png').convert_alpha()
    menu = menus.Menu((resolution[0] / 3.4, resolution[1] / 8))

    game = Game(1)
    game.blit(screen)
    pygame.display.update()
    print(resolve_velocity(60, 25))
    print(resolve_velocity(90, 25))
    print(resolve_velocity(120, 25))

    while True:
        clock.tick(60) # keep framerate at 60fps

        if menu.game_state == 'in menu':
            menu.update()
            game.blit(screen)
            menu.blit(screen)
            pygame.display.update(menu.rect)
            for event in pygame.event.get(eventtype=menus.GameCommand):
                print('button pressed event')
                if event.command == "RESTART":
                    print('Restart button')
                    game = Game(1)

        elif menu.game_state == "in game":
            game.update()
            game.blit(screen)

        pygame.display.update()
