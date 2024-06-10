import sys
from random import choice

import obstacle
import pygame
from alien import Alien
from laser import Laser
from player import Player


class Game:
    def __init__(self):
        # setup do jogador
        player_sprite = Player(
            (screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # vidas e pontuação
        self.lives = 3
        self.live_surf = pygame.image.load(
            './chronomachina/graphics/extra.png').convert_alpha()
        self.live_x_start_pos = screen_width - \
            (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('./chronomachina/font/Pixeled.ttf', 20)

        # setup do obstaculo
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        # setup do alien
        self.aliens = pygame.sprite.Group()
        self.alien_laser = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        # audio
        music = pygame.mixer.Sound('chronomachina/audio/music.mp3')
        music.set_volume(0.3)
        music.play(loops=-1)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(
                        self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for x in offset:
            self.create_obstacle(x_start, y_start, x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_laser.add(laser_sprite)

    def collision_checks(self):
        # laser do jogador
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # colisão com o obstaculo
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # colisão com o alien
                alien_hit = pygame.sprite.spritecollide(
                    laser, self.aliens, True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                    laser.kill()

                # colisão com o laser do alien
                if pygame.sprite.spritecollide(laser, self.alien_laser, True):
                    laser.kill()

        if self.alien_laser:
            for laser in self.alien_laser:
                # colisão com o obstaculo
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # colisão com o alien
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + \
                (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def victory(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('Você venceu', False, 'white')
            victory_rect = victory_surf.get_rect(
                center=(screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_laser.update()
        self.alien_position_checker()
        self.collision_checks()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_laser.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory()


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    bg = pygame.image.load('chronomachina/graphics/background.png')
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        screen.fill((30, 30, 30))
        screen.blit(bg, (0, 0))
        game.run()

        pygame.display.flip()
        clock.tick(60)
