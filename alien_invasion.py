import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from button import Button, Game_Over
from game_stats import GameStats
from scoreboard import Scoreboard, Quit_State
from pygame.sprite import Group
import random
from star import Star

def run_game():
    pygame.init()
    pygame.mixer.init()
    gf.load_sounds()
    ai_settings = Settings()
    
    # Set screen to full resolution of the display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ai_settings.screen_width = screen.get_rect().width
    ai_settings.screen_height = screen.get_rect().height
    
    pygame.display.set_caption("Alien Invasion - Sergio Edition")

    clock = pygame.time.Clock()
    FPS = 60

    ship = Ship(ai_settings, screen)
    bullets = Group()
    enemy_bullets = Group()
    aliens = Group()
    particles = Group()
    stars = Group()
    powerups = Group()
    boss_group = Group()

    for _ in range(ai_settings.star_count):
        stars.add(Star(ai_settings, screen))

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
            game_over.over = False
            # Update all game elements
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, particles, powerups, boss_group)
            gf.update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, enemy_bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over, boss_group)
            gf.update_powerups(powerups, ship)
            gf.update_boss(ai_settings, screen, boss_group, enemy_bullets, stats)
            particles.update()
            stars.update()
            
            # Additional game logic
            gf.check_collisions(bullets, enemy_bullets, aliens, ship, stats, sb, ai_settings, screen, particles, powerups, boss_group, game_over)
            
            if random.randrange(0, 65) == 1:
                gf.alien_shoot(ai_settings, screen, aliens, enemy_bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over, particles, stars, powerups, boss_group)

if __name__ == '__main__':
    run_game()
