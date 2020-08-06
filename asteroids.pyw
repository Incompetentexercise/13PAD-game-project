import pygame as pygame
import random as random


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game_resolution):
        """
        Asteroid object for game obstacles
        Each tick call:
                update()
                blit(parent surface)
        for each obstacle
        """
        super().__init__()
        self.game_resolution = game_resolution
        self.start_position = (
            random.randint(0, self.game_resolution[0]),
            -100
        )
        self.velocity = random.randint(6, 12)
        # self.velocity = 10

        # load image
        self.image = pygame.image.load(
            "images/asteroids/"+random.choice(['small', 'medium', 'large'])+".png"
        ).convert_alpha()
        # apply random rotation and scale to image
        self.image = pygame.transform.rotozoom(self.image, random.randint(0, 365), random.uniform(0.8, 1.2))
        # get bounding box
        self.rect = self.image.get_rect(center=self.start_position)

        # get mask from image
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed_multiplier):
        # update position
        self.rect.y += self.velocity*speed_multiplier
        # delete if not on screen
        if self.rect.y > self.game_resolution[1]:
            self.kill()


if __name__ == '__main__':
    def stop():
        """
        Terminate the entire program safely
        """
        pygame.quit()  # stop pygame
        exit()  # stop python

    resolution = (450, 600)  # resolution of main window
    screen = pygame.display.set_mode(resolution)  # create window
    clock = pygame.time.Clock()  # create clock object to keep frames on time
    background_image = pygame.image.load("images/game_background.png")

    obstacles = [
    ]

    while True:
        clock.tick(60)
        # screen.fill((0, 0, 0))
        screen.blit(background_image, background_image.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

        if random.randint(1, 10) == 1:
            obstacles.append(Asteroid(resolution))

        for obstacle in obstacles:
            if obstacle.update(1):
                obstacle.blit(screen)
            else:
                obstacles.remove(obstacle)


        pygame.display.update()
