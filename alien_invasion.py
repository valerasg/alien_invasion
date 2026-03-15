import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from button import Button, Game_Over
from game_stats import GameStats
from scoreboard import Scoreboard, Quit_State
from pygame.sprite import Group
import random

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion - Sergio Edition")

    clock = pygame.time.Clock()
    FPS = 60

    ship = Ship(ai_settings, screen)
    bullets = Group()
    enemy_bullets = Group()
    aliens = Group()

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    qs = Quit_State(ai_settings, screen)
    play_button = Button(ai_settings, screen, "PRESS ENTER")
    game_over = Game_Over(ai_settings, screen, "GAME OVER")

    gf.load_score(stats)
    sb.prep_high_score()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        clock.tick(FPS)
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, enemy_bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)
            
            if random.randrange(0, 65) == 1:
                gf.alien_shoot(ai_settings, screen, aliens, enemy_bullets)
            pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
            game_over.over = False

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over)

if __name__ == '__main__':
    run_game()
