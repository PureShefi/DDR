import Arrow, pygame, random, Defines

ARROW_SHOW_TIME = 0.3 * Defines.FPS

class DDRGame():
    __targetLocation = (30, 30 + Arrow.SIZE[0])

    def __init__(self, screen):
        self.arrows = []
        self.screen = screen
        self.targets = DDRGame.GetTargetArrows()
        self.keyPresses = [[0, Arrow.IMAGE]] * len(Arrow.DIRECTIONS)
        print self.keyPresses
        
    @staticmethod
    def GetTargetArrows():
        arrows = []
        for direction in Arrow.DIRECTIONS:
            arrow = Arrow.Arrow(direction, DDRGame.__targetLocation[0])
            arrows.append(arrow)

        return arrows

    def DoTurn(self):
        # Move the arrows foreward
        for arrow in self.arrows:
            arrowDir = arrow.DoTurn()

            # DoTurn returns None if arrow left the screen, so remove point on it
            if arrowDir is None:
                self.FailedDirection(arrow.GetDirection())
                self.arrows.remove(arrow)
                continue
            
            # Draw new arrow location
            self.screen.blit(arrowDir[0], arrowDir[1])

        self.DrawTargets()
        if random.randint(0, 5) == 5:
            self.AddRandomArrow()

    def AddRandomArrow(self):
        self.arrows.append(Arrow.Arrow(random.randint(0, len(Arrow.DIRECTIONS)-1)))

    def DrawTargets(self):
        # Draw the target arrows
        for direction in Arrow.DIRECTIONS:
            imageURL = Arrow.IMAGE

            # Get correct arrow image
            if self.keyPresses[direction][0] > 0:
                self.keyPresses[direction][0] -= 1
                imageURL = self.keyPresses[direction][1]

            # Add the arrow to the screen
            target = Arrow.Arrow(direction, DDRGame.__targetLocation[0], imageURL)
            self.screen.blit(target.arrow, target.arrowrect)

    @staticmethod
    def KeyToDirection(key):
        if key == pygame.K_LEFT:
            return Arrow.LEFT
        if key == pygame.K_UP:
            return Arrow.UP 
        if key == pygame.K_DOWN:
            return Arrow.DOWN
        if key == pygame.K_RIGHT:
            return Arrow.RIGHT

    def CheckIfArrowOnTarget(self, keyDirection):
        for arrow in self.arrows:
            if arrow.GetDirection() != keyDirection:
                continue

            if arrow.GetTop() > DDRGame.__targetLocation[0] and arrow.GetTop() < DDRGame.__targetLocation[1]:
                self.arrows.remove(arrow)
                self.keyPresses[keyDirection] = [ARROW_SHOW_TIME, Arrow.IMAGE_SUCCESS]
                return

        self.FailedDirection(keyDirection)

    def FailedDirection(self, keyDirection):
        self.keyPresses[keyDirection] = [ARROW_SHOW_TIME, Arrow.IMAGE_FAIL]