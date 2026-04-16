import pygame

class ClockHand:
    def __init__(self, image_path, center_pos, scale_size=None):
        """
        Initializes the clock hand.
        image_path: Path to the hand graphic.
        center_pos: (x, y) tuple for the center of the clock.
        scale_size: (width, height) tuple to resize the hand if needed.
        """
        # Load the image and preserve alpha channel for transparency
        self.original_image = pygame.image.load(image_path).convert_alpha()
        
        if scale_size:
            self.original_image = pygame.transform.scale(self.original_image, scale_size)
            
        self.image = self.original_image
        self.rect = self.image.get_rect(center=center_pos)
        self.center_pos = center_pos

    def update(self, time_value):
        """
        Calculates the angle and rotates the hand.
        time_value: The current minute or second (0-59).
        """
        # 360 degrees / 60 units = 6 degrees per unit
        angle = time_value * 6
        
        # Pygame rotates counter-clockwise. We use negative angle for clockwise rotation.
        self.image = pygame.transform.rotate(self.original_image, -angle)
        
        # Re-center the bounding box so the hand rotates around the center, not the top-left corner
        self.rect = self.image.get_rect(center=self.center_pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)