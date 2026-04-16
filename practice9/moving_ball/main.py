import pygame
import sys
from ball import Ball

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()

    ball = Ball(WIDTH, HEIGHT)

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Move on key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -ball.step)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, ball.step)
                elif event.key == pygame.K_LEFT:
                    ball.move(-ball.step, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(ball.step, 0)

        # 2. Rendering
        screen.fill(WHITE)
        ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()