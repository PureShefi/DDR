import pygame
import sys
import random

SCREEN_SIZE = WIDTH, HEIGHT = (474, 725)
WALL_DIMENSION = WALL_WIDTH, WALL_HEIGHT = (100, 500)
BIRD_DIMENSION = (30, 30)
GAP = 200
FONT_SIZE = 50
FONT_LOCATION = (((WIDTH - FONT_SIZE)/2), FONT_SIZE)

# Bird speed goes from top to bottom
WALL_SPEED = 8
GRAVITY = 0.5
BASE_SPEED = 5
CLICK_NEW_SPEED = -8
CLICK_JUMP_SIZE = 10

class FlappyBird():
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.image.load("Assets/background.jpg").convert()

        self.wallTop = pygame.image.load("Assets/top.png").convert_alpha()
        self.wallBottom = pygame.image.load("Assets/bottom.png").convert_alpha()

        self.bird = pygame.image.load("Assets/bird.png").convert_alpha()
        self.bird = pygame.transform.scale(self.bird, BIRD_DIMENSION)
        self.birdRect = self.bird.get_rect()

        self.ResetGame()


    def ResetGame(self):
        # Reset value for a new game
        self.ResetWall()
        self.jump = False
        self.birdRect.top = HEIGHT / 2
        self.birdRect.left = 10
        self.speed = BASE_SPEED
        self.dead = False
        self.score = 0

    def MoveBird(self):
        # Move the bird for the turn
        # Update new speed and location
        self.speed += GRAVITY
        self.birdRect.top += self.speed

        # Validate bird height
        if self.birdRect.top < 0 or self.birdRect.top > HEIGHT:
            self.dead = True

        # Validate bird collision with walls
        if self.birdRect.colliderect(self.rectTop) or self.birdRect.colliderect(self.rectBottom):
            self.dead = True

        # Draw the bird
        self.screen.blit(self.bird, (self.birdRect.left, self.birdRect.top))

    def MoveWall(self):
        # Move the wall for the turn
        self.wallX -= WALL_SPEED
        if self.wallX <= -WALL_WIDTH:
            self.score += 1
            self.ResetWall()

        # Get Center of screen - half of the gap + the offset
        topLocation = (HEIGHT / 2) - WALL_HEIGHT - (GAP / 2) + self.offset
        
        # Get Center of screen + half of the gap + the offset
        bottomLocation = HEIGHT - (HEIGHT / 2) + (GAP / 2) + self.offset

        self.rectTop    = pygame.Rect(self.wallX, topLocation    - 10, WALL_WIDTH, WALL_HEIGHT)
        self.rectBottom = pygame.Rect(self.wallX, bottomLocation + 10, WALL_WIDTH, WALL_HEIGHT)

        # Draw the wall
        self.screen.blit(self.wallTop, (self.wallX, topLocation))
        self.screen.blit(self.wallBottom, (self.wallX, bottomLocation))

    def ResetWall(self):
        # Reset the wall to beginning of the screen
        self.wallX = WIDTH
        self.offset = random.randint(-200, 200)

    def UpdateScore(self):
        # print score counter
        self.screen.blit(self.font.render(str(self.score),
                                     -1,
                                     (255, 255, 255)),
                                     FONT_LOCATION)
 
    def EndGame(self):
        # Draw endgame screen, just adds a white layer above
        s = pygame.Surface(SCREEN_SIZE)
        s.set_alpha(128)
        s.fill((255,255,255))
        self.screen.blit(s, (0,0))
        pygame.display.update()

    def Run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.dead = False

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    if not self.dead:
                        self.birdRect.top -= CLICK_JUMP_SIZE
                        self.speed = CLICK_NEW_SPEED
                    else:
                        self.ResetGame()

            if self.dead:
                continue

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            self.MoveWall()
            self.MoveBird()
            self.UpdateScore()
            
            if self.dead:
                self.EndGame()

            pygame.display.update()

FlappyBird().Run()