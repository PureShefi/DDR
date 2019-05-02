import pygame
import Defines

# Types of arrows
LEFT = 0
UP = 1
DOWN = 2
RIGHT = 3
DIRECTIONS = [LEFT, UP , DOWN, RIGHT]
ANGLE = [90, 0, 180, 270]

SIZE = (72, 72)
SPEED = [0, -3]
IMAGE = "Assets/Arrow.png"
IMAGE_SUCCESS = "Assets/Arrow_Success.png"
IMAGE_FAIL = "Assets/Arrow_Fail.png"
BEGGINING = Defines.SCREEN_HEIGHT - SIZE[0]

class Arrow:
    def __init__(self, direction, top=BEGGINING, url=IMAGE):
        if direction not in DIRECTIONS:
            raise "Invalid direction received"
        
        self.arrow = pygame.image.load(url)
        self.arrow = pygame.transform.scale(self.arrow, SIZE)
        self.arrow = pygame.transform.rotate(self.arrow, ANGLE[direction])

        self.arrowrect = self.arrow.get_rect()
        self.arrowrect.top = top
        self.arrowrect.left = self.CalculateArrowLocation(direction)

        self.direction = direction

    def DoTurn(self):
        self.arrowrect = self.arrowrect.move(SPEED)
        if self.arrowrect.top < 0:
            return None

        return self.arrow, self.arrowrect


    def GetTop(self):
        return self.arrowrect.top
    
    def GetDirection(self):
        return self.direction

    @staticmethod
    def CalculateArrowLocation(direction):
        if direction not in DIRECTIONS:
            raise "Invalid direction received"

        return ((Defines.SCREEN_WIDTH / len(DIRECTIONS)) * direction) + 50

