from random import randint


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5
        self.friend_speed = 1.5
        self.ship_limit = 3

        # Laser settings
        self.laser_width = 15
        self.laser_height = 3
        self.laser_speed = 3.0
        self.laser_color = (250, 5, 30)
        self.max_lasers = 3

        # Alien settings
        self.alien_speed = 1.0
        self.alien_advance = 10
        # alien_direction of 1 is down; -1 is up
        self.alien_direction = 1
        self.fleet_waves = 3

        # Target settings

        self.target_direction = 1
        self.target_width = 90
        self.target_height = 90
        self.target_color = (255, 255, 255)
        self.target_max_miss = 5
        self.target_level_up = 5

        # Game difficulty settings
        # Game speedup ratio (easy, medium, hard)
        self.speedup_ratio = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the dynamic settings for a new game."""
        self.target_speed = .5

    def speedup_game(self):
        self.target_speed *= self.speedup_ratio
