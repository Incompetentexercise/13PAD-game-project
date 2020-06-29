import pygame as pygame

pygame.init() #Start Pygame
screen = pygame.display.set_mode((600, 600)) #Start the screen

clock = pygame.time.Clock()

background = pygame.image.load("images/background.png")

running = True

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #The user closed the window!
            pygame.quit() #Close the window
            running = False
