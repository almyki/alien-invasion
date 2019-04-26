
import sys
from time import sleep

import pygame
from pygame.sprite import Sprite
from bullets import Bullet
from aliens import Alien

from pygame.sprite import Group
aliens = Group()

class GameFunctions():
    """Update positions of aliens, bullets, ship."""
    
    def __init__(self, ai_settings, screen, stats, sb, ship, aliens, bullets, 
            play_button):
        """Initialize attributes."""
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        self.sb = sb
        self.ship = ship 
        self.aliens = aliens
        self.bullets = bullets
        self.play_button = play_button
    
    def update_aliens(self):
        """
        Check if the fleet is at an edge,
          and then update the positions of all aliens in the fleet.
        """
        self.check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self.ship_hit()
            
        # Look for aliens hitting the bottom of the screen.
        self.check_aliens_bottom()

    def update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of old bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()

    def check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)

    def check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if (button_clicked and not self.stats.game_active):
                
            # Reset the game settings.
            self.ai_settings.initialize_dynamic_settings()
            
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            
            # Reset the scoreboard images.
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # Empty the list of aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()
            
            # Pause
            sleep(1.0)

    def check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif sevent.key == pygame.K_q:
            sys(exit)
                
    def fire_bullet(self):
        """Fire a bullet if limit not reached yet."""
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            # Create a new Bullet and add it to the bullets group.
            new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
                
    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()
        
    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1

    def check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, 
            False, True)
        if collisions:
            for self.aliens in collisions.values():
                self.stats.score += (self.ai_settings.alien_points 
                    * len(self.aliens))
                self.sb.prep_score()
            self.check_high_score()
            
        if len(self.aliens) == 0:
            # If the entire fleet is destroyed, start a new level.
            self.bullets.empty()
            self.ai_settings.increase_speed()
            
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            
            self.create_fleet()

    def create_new_fleet(self):
        """Destroy existing bullets and create new fleet."""
        if len(self.aliens) == 0:
            self.bullets.empty()
            self.create_fleet()

    def ship_hit(self):
        """Resets screen elements when ship is hit."""
        # Decrement ships left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            # Update scoreboard.
            self.sb.prep_ships()
            
            # Empty the list of aliens and bullets.
            self.bullets.empty()
            self.aliens.empty()
            
            # Create a new fleet and center the ship.
            self.create_fleet()
            self.ship.center_ship()
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self):
        """Check if aliens have hit the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                print("almykiVASIOOONNNNN!!!")
                # Treat this the same as if the ship got hit.
                self.ship_hit()
                break

    def update_screen(self):
        """Update images on the screen and flip to the new screen."""
        
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.ai_settings.bg_color)
        
        # Draw the play button if the game is inactive.
        if self.stats.game_active:
            # Redraw all bullets behind ship and aliens.
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            
            # Draw the score information.
            self.sb.show_score()

        else:
            self.play_button.draw_button()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()
        
    def get_number_aliens_x(self, alien_width):
        """Determine the number of aliens that fit in a row."""
        available_space_x = self.ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        available_space_y = (self.ai_settings.screen_height - 
                                (4 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        """Create a full fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self.ai_settings, self.screen)
        number_aliens_x = self.get_number_aliens_x(alien.rect.width)
        number_rows = self.get_number_rows(self.ship.rect.height, 
            alien.rect.height)
        
        # Create the fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)


print(type(aliens))
















