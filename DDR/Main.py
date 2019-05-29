import sys, pygame, time, Defines
import threading
import functools
import socket
from DDRGame import DDRGame

pygame.init()
screen = pygame.display.set_mode(Defines.SCREEN_SIZE)

gameInstance = DDRGame(screen)
clock = pygame.time.Clock()

msgs = set()
msgs_lock = threading.Lock()


def pump():
    moves_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    moves_socket.setblocking(1)
    moves_socket.bind(('0.0.0.0', 1337))
    for direction in iter(functools.partial(moves_socket.recv, 10), ''):
        direction = int(direction)
        with msgs_lock:
            msgs.add(direction)


threading.Thread(target=pump).start()

while 1:
    clock.tick(60)

    screen.fill(Defines.WHITE)
    gameInstance.DoTurn()

    with msgs_lock:
        for direction in msgs:
            print(direction)
            gameInstance.CheckIfArrowOnTarget(direction)
        msgs.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            gameInstance.CheckIfArrowOnTarget(DDRGame.KeyToDirection(event.key))

    pygame.display.flip()
