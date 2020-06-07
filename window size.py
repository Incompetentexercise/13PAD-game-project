import pygame as pyg

pyg.init() #Start Pygame
screen = pyg.display.set_mode((600, 600)) #Start the screen

clock = pyg.time.Clock()

background = pyg.image.load("images/background.png")

running = True

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    pyg.display.flip()

    for event in pyg.event.get():
        if event.type == pyg.QUIT: #The user closed the window!
            pyg.quit() #Close the window
            running = False
