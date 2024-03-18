import sys

import pygame


class Game:
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
