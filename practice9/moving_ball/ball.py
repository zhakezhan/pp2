import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 25
        self.color = (255, 0, 0)  # Red
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Start ball in the center
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.step = 20

    def move(self, dx, dy):
        """Moves the ball if the new position is within boundaries."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Boundary Check: Ensure the edges of the ball don't cross the screen limits
        if (self.radius <= new_x <= self.screen_width - self.radius) and \
           (self.radius <= new_y <= self.screen_height - self.radius):
            self.x = new_x
            self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)