import pygame as pygame
import pygame_menu


def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))

        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
