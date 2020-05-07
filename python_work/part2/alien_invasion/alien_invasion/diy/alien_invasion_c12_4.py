import sys

import pygame

from settings import Settings
from ship import Ship
from friend import Friend

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

        self.ship = Ship(self)
        self.friend = Friend(self)

        # Set the background color. 
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()
            self.ship.update()
            self.friend.update()
            self._update_screen()
            

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:            
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
#            self.friend.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
#            self.friend.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit(0)
        elif event.key == pygame.K_s: #12.4
            if self.ship.active == True:
                self.ship.active = False
                self.friend.active = True
            elif self.ship.active == False:
                self.ship.active = True #12.4
                self.friend.active = False
        elif event.key == pygame.K_UP: #12.4
            self.ship.moving_up = True #12.4
            self.friend.moving_up = True
        elif event.key == pygame.K_DOWN: #12.4
            self.ship.moving_down = True
            self.friend.moving_down = True



    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.friend.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False   
            self.friend.moving_left = False
        elif event.key == pygame.K_UP: #12.4
            self.ship.moving_up = False #12.4
            self.friend.moving_up = False
        elif event.key == pygame.K_DOWN: #12.4
            self.ship.moving_down = False
            self.friend.moving_down = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.friend.blitme()
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()