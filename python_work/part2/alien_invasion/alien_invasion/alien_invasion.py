import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from laser import Laser
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create a game resources."""
        pygame.init()
        self.settings = Settings()

        # This block is for windowed mode
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # This block is for full screen mode.
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #  and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make the Start game buttons.
        self.game_buttons = []
        # self.play_button = Button(self, "Play")
        # self.easy_button = Button(self, "Easy")
        # self.medium_button = Button(self, "Medium")
        # self.hard_button = Button(self, "Hard")

        self._create_fleet()
        self._make_game_buttons()

    def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and lasers.
        self.aliens.empty()
        self.lasers.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Initialize game settings and game screen template.
        self.settings.initialize_dynamic_settings(self.difficulty)
        self.sb.prep_images()

        # Flip the flag to show the play button after this game.
        self.stats.show_play = 1

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_lasers()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                old_high_score = self.stats._get_high_score()
                if old_high_score < self.stats.high_score:
                    self.stats._export_high_score()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.stats.show_play:
                    self._check_play_button(mouse_pos)
                else:
                    self._check_difficulty_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _make_game_buttons(self):
        for button in self.settings.button_text:
            new_button = Button(self, button)
            self.game_buttons.append(new_button)

    def _check_play_button(self, mouse_pos):
        """Prompt for difficulty when the player clicks Play."""
        button_clicked = self.game_buttons[0].rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Prompt for game difficulty.
            self.stats.show_play = 0
            # self._check_difficulty_button(mouse_pos)

    def _check_difficulty_button(self, mouse_pos):
        """Start game at chosen difficulty of player selection."""
        easy_button_clicked = self.game_buttons[1].rect.collidepoint(mouse_pos)
        medium_button_clicked = self.game_buttons[2].rect.collidepoint(
            mouse_pos)
        hard_button_clicked = self.game_buttons[3].rect.collidepoint(mouse_pos)

        if easy_button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.difficulty = 'easy'
            self._start_game()
        elif medium_button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.difficulty = 'medium'
            self._start_game()
        elif hard_button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.difficulty = 'hard'
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            old_high_score = self.stats._get_high_score()
            if old_high_score < self.stats.high_score:
                self.stats._export_high_score()
            sys.exit(0)
        elif event.key == pygame.K_SPACE:
            self._fire_laser()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_laser(self):
        """Create a new laser and add it to the lasers group."""
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_lasers(self):
        """Update position of lasers and get rid of old lasers."""
        # Update laser postitions.
        self.lasers.update()

        # Get rid of lasers that have disappeared.
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        self._check_laser_alien_collisions()

    def _check_laser_alien_collisions(self):
        """Respond to laser-alien collisions."""
        # Remove any lasers and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens,
            self.settings.laser_collide_remove, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        self._start_new_level()

    def _start_new_level(self):
        # Remove existing lasers and create a new fleet
        if not self.aliens:
            self.lasers.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and determine the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height
                             - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, then update the positions of all
        aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and lasers.
            self.aliens.empty()
            self.lasers.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _draw_buttons(self):
        if self.stats.show_play:
            self.game_buttons[0].draw_button()
        else:
            for button in range(1, len(self.settings.button_text)):
                self.game_buttons[button].rect.centerx = int((
                    self.settings.screen_width / 2) - (
                    self.game_buttons[button].width * 1.5) * (2 - button))
                self.game_buttons[button].msg_image_rect.centerx = int((
                    self.settings.screen_width / 2) - (
                    self.game_buttons[button].width * 1.5) * (2 - button))
                self.game_buttons[button].draw_button()

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self._draw_buttons()

        # Everything needs to be drawn before .flip
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
