import pygame as pygame
import json


# with open('settings.json') as settings_file:
#     settings = json.load(settings_file)
#
# background_color = tuple(settings['window']['background color'])
# background_image = pygame.image.load(settings['window']['background image'])
# resolution = tuple(settings['window']['resolution'])


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 600))

    while True:
        clock.tick(60)
        screen.fill((11, 4, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
