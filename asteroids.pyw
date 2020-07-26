import pygame as pygame
import random as random


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        """
        Asteroid object for game obstacles
        Each tick call:
                update()
                blit(parent surface)
        for each obstacle
        """
        super().__init__()
        self.start_position = (
            random.randint(0, resolution[0]),
            -100
        )
        self.velocity = random.randint(2, 3)

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

    def update(self):
        # update position
        self.rect.y += self.velocity
        # delete if not on screen
        if self.rect.y > resolution[1]:
            obstacles.remove(self)

    def blit(self, surface):
        # draw onto given surface
        surface.blit(self.image, self.rect)


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
        Asteroid(),
        Asteroid()
    ]

    while True:
        clock.tick(30)
        # screen.fill((0, 0, 0))
        screen.blit(background_image, background_image.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #The user closed the window!
                stop()

        if random.randint(1, 50) == 1:
            obstacles.append(Asteroid())

        for obstacle in obstacles:
            obstacle.update()
            obstacle.blit(screen)

        pygame.display.update()
