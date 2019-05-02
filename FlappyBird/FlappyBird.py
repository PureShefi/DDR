import pygame
import sys

class FlappyBird():
    def __init__(self):
        self.screen = pygame.display.set_mode((474, 725))
        self.background = pygame.image.load("Assets/background.jpg").convert()


    def Run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    pass

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            pygame.display.update()

FlappyBird().Run()