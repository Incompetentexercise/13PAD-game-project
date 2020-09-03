import pygame as pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("images/ship_jet.png").convert_alpha()

        # A reference to the original image to preserve the quality.
        self.orig_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0

    def update(self):
        self.angle += 2
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)


def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group(Entity((320, 240)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
