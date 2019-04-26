
class Settings():
    """A class to store all settings for almykivasion!!!"""
    
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 300
        self.screen_height = 250
        self.bg_color = (10, 5, 20)
        
        # Ship Settings
        self.ship_limit = 1
        
        # Bullet Settings
        self.bullet_width = 2
        self.bullet_height = 10
        self.bullet_color = 255, 240, 0
        self.bullets_allowed = 3
        
        # Alien Settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2
        # How quickly the alien point values increase.
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 0.2
        self.bullet_speed_factor = 0.5
        self.alien_speed_factor = 0.01
        
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        # Scoring
        self.alien_points = 50
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
