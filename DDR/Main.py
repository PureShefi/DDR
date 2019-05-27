import sys, pygame, time, Defines
import time
from DDRGame import DDRGame
pygame.init()
screen = pygame.display.set_mode(Defines.SCREEN_SIZE)

gameInstance = DDRGame(screen)
clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            gameInstance.CheckIfArrowOnTarget(DDRGame.KeyToDirection(event.key))

    screen.fill(Defines.WHITE)

    gameInstance.DoTurn()

    pygame.display.flip()
