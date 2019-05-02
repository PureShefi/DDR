import pygame
import sys
import random

SCREEN_SIZE = WIDTH, HEIGHT = (474, 725)
WALL_DIMENSION = WALL_WIDTH, WALL_HEIGHT = (100, 500)
GAP = 100

class FlappyBird():
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.image.load("Assets/background.jpg").convert()

        self.wallTop = pygame.image.load("Assets/top.png").convert_alpha()
        self.wallBottom = pygame.image.load("Assets/bottom.png").convert_alpha()

        self.bird = pygame.image.load("Assets/bird.png").convert_alpha()
        self.bird = pygame.transform.scale(self.bird, (100, 100))

        self.ResetWall()

        self.jump = False
        self.birdX = 0
        self.birdY = HEIGHT / 2
        self.gravity = 0.5
        self.speed = 5

    def MoveBird(self):
        # Move the bird for the turn
        if self.jump:
            self.birdY -= 5
            self.jump = False

        self.speed += self.gravity
        self.birdY += self.speed

        self.screen.blit(self.bird, (self.birdX, self.birdY))

    def MoveWall(self):
        # Move the wall for the turn
        self.wallX -= 10
        if self.wallX <= -WALL_WIDTH:
            self.ResetWall();

        # Get Center of screen - half of the gap + the offset
        topLocation = (HEIGHT / 2) - WALL_HEIGHT - (GAP / 2) + self.offset
        
        # Get Center of screen + half of the gap + the offset
        bottomLocation = HEIGHT - (HEIGHT / 2) + (GAP / 2) + self.offset

        # Draw the wall
        self.screen.blit(self.wallTop, (self.wallX, topLocation))
        self.screen.blit(self.wallBottom, (self.wallX, bottomLocation))

    def ResetWall(self):
        # Reset the wall to beginning of the screen
        self.wallX = WIDTH
        self.offset = random.randint(-150, 100)
 

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
                    self.jump = True
                    self.speed = -10


            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            self.MoveWall()
            self.MoveBird()
            
            pygame.display.update()

FlappyBird().Run()