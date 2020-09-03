import pygame as pygame
import menus
import asteroids
from math import sin, cos, radians
import random as random

GENERATE_OBSTACLE = pygame.USEREVENT+3 # event type for generating obstacle
GENERATE_FUEL = pygame.USEREVENT+6


def resolve_velocity(direction, speed):
    """
    Resolve a vector (direction, speed) into x, y components
    Give direction in degrees
            0deg --> left
            90deg --> up
            180deg --> right
            >360deg illegal
    Give speed as pixels/second
    """
    if 0 > direction > 180: # bullet would be travelling down, not okay.
        return 'why?'
    elif direction < 90:
        __x = -speed*cos(radians(direction))
        __y = speed * sin(radians(direction))
    else:
        __x = speed*cos(radians(180 - direction))
        __y = speed*sin(radians(180 - direction))

    return __x, __y


def stop():
    """ Terminate the entire program safely """
    pygame.quit() # stop pygame
    exit() # stop python


def check_collisions(primary, secondaries):
    """
    Check for collisions between a sprite and a group of sprites
        Primary is a single sprite
        Secondaries is a sprite group
    does collision check using masks
    for efficiency, each sprite should have a mask generated when it is created

    Returns a list of secondary sprites that are colliding with the primary sprite
    Does NOT delete colliding sprites
    """
    collisions = pygame.sprite.spritecollide(primary, secondaries, False, pygame.sprite.collide_mask)
    return collisions


# class Decorative(pygame.sprite.Sprite):
#     def __init__(self, position, image_path, lifetime):
#         super().__init__()
#         self.position = position
#         self.image = pygame.image.load(image_path).convert_alpha()
#         self.rect = self.image.get_rect()
#         self.lifetime = lifetime
#         self.starting_time = pygame.time.get_ticks()
#
#     def update(self, speed_multiplier):
#         if pygame.time.get_ticks()-self.starting_time > self.lifetime:
#             self.kill()


class FuelBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = (20, 20)
        self.fuel_amount = 8
        self.images = []
        for i in range(0, 9):
            self.images.append(pygame.image.load('images/fuel_bar/'+str(i)+'.png').convert_alpha())
        self.image = self.images[self.fuel_amount]
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, speed):
        if self.fuel_amount > 0:
            self.fuel_amount -= 0.006 * speed
        self.image = self.images[int(round(self.fuel_amount))]

    def modify(self, amount):
        if amount > 0:
            if self.fuel_amount+amount < 8.5:
                self.fuel_amount += amount
        elif amount < 0:
            if self.fuel_amount+amount > 0:
                self.fuel_amount += amount


class FuelBarrel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = (random.randint(0, resolution[0]), -52)
        self.speed = random.randint(8, 10)
        self.image = pygame.image.load('images/fuel_barrel/fuel_barrel.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed_multiplier):
        # update position
        self.rect.y += self.speed * speed_multiplier
        # delete if not on screen
        if self.rect.y > resolution[1]:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        """
        A bullet fired at asteroids by the player's ship
        """
        super().__init__() # initialize sprite parent class
        self.position = list(position) # make a copy of the given position
        # load own images, each is slightly different for animation
        self.images = [
            pygame.image.load('images/bullets/0.png').convert_alpha(),
            pygame.image.load('images/bullets/1.png').convert_alpha(),
            pygame.image.load('images/bullets/2.png').convert_alpha()
        ]
        # counter to keep track of when to switch images
        #       <10 img 0
        #       >=10<20 img 1
        #       >=20<30 img 2
        self.image_counter = 0
        self.image = self.images[self.image_counter]
        self.rect = self.image.get_rect(center=self.position)
        # all the images have a very similar mask so only one needs to be generated
        self.mask = pygame.mask.from_surface(pygame.image.load('images/bullets/mask.png').convert_alpha())

        self.direction = direction
        self.speed = 25
        self.move_amount = (0, 0) # amount to move this tick

    def update(self, speed_multiplier):
        """
        update position and image
        """
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
        self.horizontal_speed = 5 # how fast the player can move to the side
        self.position = [resolution[0]/2, resolution[1]-50] # center bottom
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

        if game.fuel_bar.fuel_amount < 1:
            speed_multiplier *= 0.3
        if speed_multiplier > 1:
            self.speed = 'fast'
        else:
            self.speed = 'slow'
        self.image = self.images[self.direction][self.speed] # pick image based on direction and speed
        self.mask = pygame.mask.from_surface(self.image) # update collision mask

        if self.direction == 'left':
            # move left
            if self.position[0] >= 0:
                # if not at left edge
                self.position[0] -= self.horizontal_speed*speed_multiplier
        elif self.direction == 'right':
            # move right
            if self.position[0] <= resolution[0]:
                # if not at right edge
                self.position[0] += self.horizontal_speed*speed_multiplier

        self.rect = self.image.get_rect(center=self.position) # place rect at new position

    def shoot(self):
        """
        Initialize a bullet in the correct place and direction
        """
        if self.direction == 'left':
            self.__temp_bullet = Bullet(self.position, 60)
        elif self.direction == 'forward':
            self.__temp_bullet = Bullet(self.position, 90)
        else:
            self.__temp_bullet = Bullet(self.position, 120)
        global game
        game.sprites.add(self.__temp_bullet)
        game.bullets.add(self.__temp_bullet)
        game.fuel_bar.modify(-1)
        sounds['phaser'].play()


class Game:
    def __init__(self, difficulty):
        """
        Manages all the gamey parts of the program that the player can actually play
        """
        # load background
        self.background_image = pygame.image.load('images/game_background.png')
        # make a copy of the background to avoid changing the original
        self.surface = self.background_image.copy()

        # set a timer that posts the generate obstacle event at an interval depending on difficulty
        pygame.time.set_timer(GENERATE_OBSTACLE, int(200 / difficulty))
        # set a timer for generating fuel cans, interval increased for higher difficulties
        pygame.time.set_timer(GENERATE_FUEL, int(1500*difficulty))

        self.top_layer = pygame.sprite.Group() # group for rendering sprites above everything else
        self.asteroids = pygame.sprite.Group() # asteroids only, for group collisions
        self.bullets = pygame.sprite.Group() # bullets only, for group collisions
        self.fuel_cans = pygame.sprite.Group() # fuel cans only, for group collisions
        self.sprites = pygame.sprite.Group() # ALL sprites, updates and draws first each tick

        self.__collision_holder = None  # holds colliding sprites temporarily

        self.player = Player()
        self.sprites.add(self.player)

        self.fuel_bar = FuelBar()
        self.sprites.add(self.fuel_bar)
        self.top_layer.add(self.fuel_bar)

        self.speed_multiplier = 1 # depends on whether a go-faster key is pressed
        self.speed_multiplier_multiplier = 1*difficulty # used to gradually increase the speed
        self.pressed_keys = None

    def update(self):
        """
        Update the game state
        Updates all the objects in the game
        Handles all events for a tick
        """
        # clear surface with clean background
        self.surface.blit(self.background_image, self.background_image.get_rect())
        self.speed_multiplier_multiplier += 0.0001 # gradually increase speed

        # handle all the events from this tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()
            if event.type == pygame.KEYDOWN:
                # key was pressed down on this tick
                if event.key in [pygame.K_ESCAPE]:
                    # the player has paused the game. Enter pause menu
                    menu.game_state = 'in menu'
                    menu.state = 'paused'
                elif event.key == pygame.K_SPACE:
                    if self.fuel_bar.fuel_amount > 1:
                        self.player.shoot()
            elif event.type == GENERATE_OBSTACLE:
                __asteroid = asteroids.Asteroid(resolution) # create a temporary pointer to new asteroid
                # add new asteroid to sprite lists for updating an rendering
                self.asteroids.add(__asteroid)
                self.sprites.add(__asteroid)
            elif event.type == GENERATE_FUEL:
                __fuel_can = FuelBarrel()
                self.fuel_cans.add(__fuel_can)
                self.sprites.add(__fuel_can)

        self.pressed_keys = pygame.key.get_pressed() # get a list of all the keys currently held down

        # if any valid keys for speed increase are pressed
        if self.pressed_keys[pygame.K_UP] or self.pressed_keys[pygame.K_w] or self.pressed_keys[pygame.KMOD_SHIFT]:
            if self.fuel_bar.fuel_amount > 1:
                self.speed_multiplier = 1.8 # the asteroids should move slightly faster
            else:
                self.speed_multiplier = 1
        else:
            self.speed_multiplier = 1

        # update all the sprites and give them the speed multiplier
        # multiply speed multiplier again to increase speed as the game continues
        self.sprites.update(self.speed_multiplier*self.speed_multiplier_multiplier)
        # test for collisions between bullets and asteroids, delete colliding sprites
        pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True, pygame.sprite.collide_mask)

        self.sprites.draw(self.surface) # draw all game sprites to game surface
        self.top_layer.draw(self.surface)

        self.__collision_holder = check_collisions(self.player, self.fuel_cans)
        if self.__collision_holder:
            for can in self.__collision_holder:
                can.kill()
                self.fuel_bar.modify(1)

        # if player is colliding with an asteroid they have lost the round, go to death menu
        if check_collisions(self.player, self.asteroids):
            menu.game_state = 'in menu'
            menu.state = 'death'

    def blit(self, surface):
        surface.blit(self.surface, self.surface.get_rect())


if __name__ == '__main__':
    pygame.font.init()
    resolution = (450, 600)
    screen = pygame.display.set_mode(resolution) # game window
    clock = pygame.time.Clock()
    pygame.mixer.init(44100, 16, 4, 2) # initialize the sound module
    sounds = {
        'phaser': pygame.mixer.Sound('sounds/phaser.wav')
    }

    # create menu object to handle menu pages
    menu = menus.Menu((resolution[0] / 3.4, resolution[1] / 8))
    # make game object with default difficulty, mostly for rendering initial background
    game = Game(1)

    # main loop
    while True:
        clock.tick(60) # keep framerate at 60fps
        # the program is in any menu page
        if menu.game_state == 'in menu':
            menu.update()
            game.blit(screen) # draw game behind menu
            menu.blit(screen) # draw menu in foreground

            # check for game play or restart buttons being pressed
            for event in pygame.event.get(eventtype=menus.GameCommand):
                if event.command == "RESTART":
                    # start or restart the game
                    if menu.difficulty == 'EASY':
                        game = Game(0.65) # on easy difficulty
                    elif menu.difficulty == 'MEDIUM':
                        game = Game(0.8) # slightly harder
                    elif menu.difficulty == 'HARD':
                        game = Game(1.15)
                    elif menu.difficulty == 'expert':
                        game = Game(1.85) # hardest, kinda nuts

        elif menu.game_state == "in game":
            game.update()
            game.blit(screen)

        pygame.display.update() # display screen changes to player
