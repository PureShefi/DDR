import pygame
import sys
import random
import socket
import pickle

SOCKET_TARGET_HOST = ('127.0.0.1', 7891)
LOCAL_SOCKET_HOST = ('0.0.0.0', 7892)
SCREEN_SIZE = WIDTH, HEIGHT = (474, 725)
WALL_DIMENSION = WALL_WIDTH, WALL_HEIGHT = (100, 500)
BIRD_DIMENSION = (30, 30)
GAP = 200
FONT_SIZE = 50
FONT_LOCATION = (((WIDTH - FONT_SIZE) / 2), FONT_SIZE)
NOTIFICATION_FONT_SIZE = FONT_SIZE / 2

# Bird speed goes from top to bottom
WALL_SPEED = 8
GRAVITY = 0.5
BASE_SPEED = 5
CLICK_NEW_SPEED = -8
CLICK_JUMP_SIZE = 10
scoreboard_file = '../scoreboard.pkl'

pygame.font.init()
FONT = pygame.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.hint_surface = FONT.render("Submit name:", True, self.color)

    def handle_event(self, event):
        enterPressed = ""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                enterPressed = self.text
                print(self.text)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)

        return enterPressed

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        screen.blit(self.hint_surface, (self.rect.x, self.rect.y - 25))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class FlappyBird():
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.image.load("Assets/background.jpg").convert()

        self.wallTop = pygame.image.load("Assets/top.png").convert_alpha()
        self.wallBottom = pygame.image.load("Assets/bottom.png").convert_alpha()

        self.bird = pygame.image.load("Assets/bird.png").convert_alpha()
        self.bird = pygame.transform.scale(self.bird, BIRD_DIMENSION)
        self.birdRect = self.bird.get_rect()

        self.space_update_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.score_updates_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.score_updates_socket.bind(LOCAL_SOCKET_HOST)
        self.score_updates_socket.settimeout(0)

        self.name_input = InputBox(100, 200, 300, 32)
        with open(scoreboard_file, 'rb') as f:
            self.scoreboard = pickle.load(f)

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

        self.rectTop = pygame.Rect(self.wallX, topLocation - 10, WALL_WIDTH, WALL_HEIGHT)
        self.rectBottom = pygame.Rect(self.wallX, bottomLocation + 10, WALL_WIDTH, WALL_HEIGHT)

        # Draw the wall
        self.screen.blit(self.wallTop, (self.wallX, topLocation))
        self.screen.blit(self.wallBottom, (self.wallX, bottomLocation))

    def ResetWall(self):
        # Reset the wall to beginning of the screen
        self.wallX = WIDTH
        self.offset = random.randint(-200, 200)

    def UpdateScore(self):
        try:
            result = self.score_updates_socket.recv(1514)
            if result == '+':
                self.score += 0.5
            elif result:
                self.score -= 1
        except socket.error:
            pass

        # print score counter
        self.screen.blit(self.font.render(str(self.score),
                                          -1,
                                          (255, 255, 255)),
                         FONT_LOCATION)

    def PrintNotification(self, notification):
        # print score counter
        notification_location = WIDTH / 4, HEIGHT / 8
        self.screen.blit(self.notification_font.render(notification,
                                                       -1,
                                                       (255, 255, 255)),
                         notification_location)

    def EndGame(self):
        # Draw endgame screen, just adds a white layer above
        s = pygame.Surface(SCREEN_SIZE)
        s.set_alpha(128)
        s.fill((255, 255, 255))
        self.screen.blit(s, (0, 0))
        pygame.display.update()

    def Run(self):
        self.EndGame()
        clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.notification_font = pygame.font.SysFont("Arial", NOTIFICATION_FONT_SIZE)
        self.dead = True
        self.EndGame()

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    if not self.dead:
                        self.birdRect.top -= CLICK_JUMP_SIZE
                        self.speed = CLICK_NEW_SPEED
                        self.space_update_socket.sendto('', SOCKET_TARGET_HOST)
                    else:
                        if self.score:
                            currentPlayer = self.name_input.handle_event(event)
                            if currentPlayer:
                                self.scoreboard.append((self.score, 'Game ' + str(len(self.scoreboard))))
                                self.scoreboard.sort(key=lambda x: x[0], reverse=True)
                                with open(scoreboard_file, 'wb') as f:
                                    pickle.dump(self.scoreboard, f)
                                print self.scoreboard
                                self.ResetGame()
                        else:
                            self.ResetGame()

            if self.dead:
                if self.score:
                    self.name_input.draw(self.screen)
                else:
                    self.PrintNotification("Press space to start")
                pygame.display.update()
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
