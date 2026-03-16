import sys
from time import sleep
import pygame
from bullet import Bullet
from bullet import Enemy_Bullet
from alien import Alien
import random
from particle import Particle
from powerup import PowerUp
from boss import Boss

sounds = {}

def load_sounds():
    try:
        sounds['shoot'] = pygame.mixer.Sound('shoot.wav')
        sounds['explosion'] = pygame.mixer.Sound('explosion.wav')
        sounds['powerup'] = pygame.mixer.Sound('powerup.wav')
        pygame.mixer.music.load('bgm.wav')
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Error loading sounds:", e)

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    if event.key == pygame.K_q:
        save_high_score(stats)
        sys.exit()
    if stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_UP:
            ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)

def save_high_score(stats):
    filename = 'highscore.txt'
    with open(filename, 'w') as file_object:
        file_object.write(str(stats.high_score))

def start_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, event, sb, enemy_bullets):
    if not stats.game_active:
        if event.key == pygame.K_RETURN:
            reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        ship.shots_fired += 1
        is_super = (ship.shots_fired % ai_settings.shots_to_super == 0)
        new_bullet = Bullet(ai_settings, screen, ship, is_super)
        bullets.add(new_bullet)
        if 'shoot' in sounds:
            sounds['shoot'].play()
        if ship.powerup_timers['multi_shot'] > 0:
            bullets.add(Bullet(ai_settings, screen, ship, is_super, dx=-2))
            bullets.add(Bullet(ai_settings, screen, ship, is_super, dx=2))

def update_powerups(powerups, ship):
    powerups.update()
    for powerup in powerups.copy():
        if powerup.rect.top >= ship.ai_settings.screen_height:
            powerups.remove(powerup)
    
    collisions = pygame.sprite.spritecollide(ship, powerups, True)
    for powerup in collisions:
        # Give 600 frames (10 seconds) of the powerup
        ship.powerup_timers[powerup.type] = 600
        if 'powerup' in sounds:
            sounds['powerup'].play()

def alien_shoot(ai_settings, screen, aliens, enemy_bullets):
    if len(enemy_bullets) < ai_settings.enemy_bullets_allowed:
        new_bullet = Enemy_Bullet(ai_settings, screen, aliens)
        enemy_bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
            start_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, event, sb, enemy_bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, event, sb, enemy_bullets)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, event, sb, enemy_bullets):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets)

def reset_game(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    enemy_bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over, particles, stars, powerups, boss_group):
    screen.fill(ai_settings.bg_color)
    for star in stars.sprites():
        star.draw_star()
    ship.blitme()
    aliens.draw(screen)
    for boss in boss_group.sprites():
        boss.blitme()
    for particle in particles.sprites():
        particle.draw_particle()
    for powerup in powerups.sprites():
        powerup.draw_powerup()
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for enemy_bullet in enemy_bullets.sprites():
        enemy_bullet.draw_enemy_bullet()
    if not stats.game_active:
        play_button.draw_button()
        qs.show_quit()
    if game_over.over:
        game_over.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, particles, powerups, boss_group):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, particles, powerups, boss_group)

def update_enemy_bullets(ai_settings, screen, stats, sb, ship, aliens, enemy_bullets):
    enemy_bullets.update()
    for enemy_bullet in enemy_bullets.copy():
        if enemy_bullet.rect.top >= ai_settings.screen_height:
            enemy_bullets.remove(enemy_bullet)

def check_collisions(bullets, enemy_bullets, aliens, ship, stats, sb, ai_settings, screen, particles, powerups, boss_group, game_over):
    """Respond to bullet-bullet, bullet-alien, and alien-ship collisions."""
    # Bullet-bullet collisions
    pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
    
    # Bullet-alien and bullet-boss collisions
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, particles, powerups, boss_group)
    
    # Alien/Boss-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens) or \
       pygame.sprite.spritecollideany(ship, enemy_bullets) or \
       pygame.sprite.spritecollideany(ship, boss_group):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, particles, powerups, boss_group):
    # Check regular aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        if 'explosion' in sounds:
            sounds['explosion'].play()
        for collided_aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(collided_aliens)
            sb.prep_score()
            for alien in collided_aliens:
                for _ in range(15):
                    new_particle = Particle(screen, alien.rect.centerx, alien.rect.centery)
                    particles.add(new_particle)
                # 15% chance to drop a powerup
                if random.random() < 0.15:
                    new_powerup = PowerUp(ai_settings, screen, alien.rect.centerx, alien.rect.centery)
                    powerups.add(new_powerup)
        check_high_score(stats, sb)

    # Check boss
    boss_collisions = pygame.sprite.groupcollide(bullets, boss_group, True, False)
    if boss_collisions:
        for bosses in boss_collisions.values():
            for boss in bosses:
                # Add damage particles
                for _ in range(5):
                    particles.add(Particle(screen, boss.rect.centerx, boss.rect.bottom))
                # Take damage
                destroyed = boss.take_damage(10)
                if destroyed:
                    if 'explosion' in sounds:
                        sounds['explosion'].play()
                    boss_group.remove(boss)
                    stats.score += 1000 * stats.level
                    sb.prep_score()
                    # Explosion particles
                    for _ in range(50):
                        particles.add(Particle(screen, boss.rect.centerx, boss.rect.centery, color=(255, 0, 0)))

    if len(aliens) == 0 and len(boss_group) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        # Every 3 levels spawn Boss, else normal fleet
        if stats.level % 3 == 0:
            boss_group.add(Boss(ai_settings, screen, stats.level))
        else:
            create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    # Limit to maximum 10-12 columns to prevent overcrowding on large screens
    return min(number_aliens_x, 12)

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (4 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    # Limit to maximum 5-6 rows
    return min(number_rows, 5)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 30
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)
            break

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over):
    if ship.powerup_timers['shield'] > 0:
        ship.powerup_timers['shield'] = 0
        bullets.empty()
        enemy_bullets.empty()
        # Move aliens up a bit to give player space
        if aliens:
            first_alien = aliens.sprites()[0]
            offset = first_alien.rect.top - 110
            for alien in aliens:
                alien.rect.top -= offset
        sleep(0.6)
        return

    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        bullets.empty()
        enemy_bullets.empty()
        ship.center_ship()
        # Move aliens up a bit to give player space
        if aliens:
            first_alien = aliens.sprites()[0]
            offset = first_alien.rect.top - 110
            for alien in aliens:
                alien.rect.top -= offset
        sleep(0.6)
    else:
        stats.ships_left = -1
        sb.prep_ships()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        game_over.over = True

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over, boss_group):
    """Update position of all aliens and check for bottom collisions."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, enemy_bullets, game_over)

def update_boss(ai_settings, screen, boss_group, enemy_bullets, stats):
    boss_group.update()
    for boss in boss_group.sprites():
        if boss.check_edges():
            boss.direction *= -1
        # Boss shooting logic
        if random.randrange(0, 30) == 1:
            if len(enemy_bullets) < ai_settings.enemy_bullets_allowed * 2:
                new_bullet = Enemy_Bullet(ai_settings, screen, [boss])
                enemy_bullets.add(new_bullet)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def load_score(stats):
    filename = 'highscore.txt'
    try:
        with open(filename) as file_object:
            score = file_object.read()
            stats.high_score = int(score)
    except (FileNotFoundError, ValueError):
        pass
