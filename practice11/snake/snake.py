import pygame
import random
import time

# Initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: Weighted & Timed Edition")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 25)
level_font = pygame.font.SysFont("Arial", 50, bold=True)

class SnakeGame:
    def __init__(self):
        # Initial snake: head and two body segments
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.speed = 10
        
        # Food attributes
        self.food_pos = [0, 0]
        self.food_weight = 1
        self.food_spawn_time = 0
        self.food_timer_limit = 5000  # 5 seconds in milliseconds
        
        self.spawn_food()

    def spawn_food(self):
        """Generates food with random weight and resets the life-timer."""
        while True:
            pos = [
                random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            ]
            # Ensure food doesn't spawn on the snake's body
            if pos not in self.snake:
                self.food_pos = pos
                break
        
        # TASK: Randomly generating food with different weights
        self.food_weight = random.randint(1, 3) 
        
        # TASK: Record the time when food was created for the timer
        self.food_spawn_time = pygame.time.get_ticks()

    def update(self):
        """Game logic update: movement, collisions, and timers."""
        
        # TASK: Check if food should disappear after some time
        current_time = pygame.time.get_ticks()
        if current_time - self.food_spawn_time > self.food_timer_limit:
            self.spawn_food() # Food 'disappears' and moves to a new spot

        head = list(self.snake[0])

        # Directional Movement
        if self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE

        # 1. Wall Collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return False

        # 2. Self-Collision
        if head in self.snake:
            return False

        self.snake.insert(0, head)

        # 3. Eating Food
        if head == self.food_pos:
            # Increase score by the weight of the food
            self.score += self.food_weight
            
            # Logic for Leveling Up (every 5 points)
            if self.score // 5 >= self.level:
                self.level += 1
                self.speed += 2
                self.flash_level_up()
            
            self.spawn_food()
        else:
            # Move the tail if no food eaten
            self.snake.pop()
        
        return True

    def flash_level_up(self):
        """Visual feedback when leveling up."""
        text = level_font.render(f"LEVEL {self.level}!", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.flip()
        time.sleep(0.3)

def main():
    game = SnakeGame()
    running = True

    while running:
        screen.fill(BLACK)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != "DOWN":
                    game.direction = "UP"
                elif event.key == pygame.K_DOWN and game.direction != "UP":
                    game.direction = "DOWN"
                elif event.key == pygame.K_LEFT and game.direction != "RIGHT":
                    game.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and game.direction != "LEFT":
                    game.direction = "RIGHT"

        # Logic Update
        if not game.update():
            msg = level_font.render("GAME OVER", True, RED)
            screen.blit(msg, (WIDTH // 2 - 140, HEIGHT // 2 - 30))
            pygame.display.flip()
            time.sleep(2)
            running = False

        # DRAWING
        # Draw Snake
        for block in game.snake:
            pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # Draw Food
        # The size of the food changes based on its weight
        food_size_mod = game.food_weight * 4
        food_rect = (
            game.food_pos[0] + (BLOCK_SIZE - food_size_mod)//2, 
            game.food_pos[1] + (BLOCK_SIZE - food_size_mod)//2, 
            food_size_mod, 
            food_size_mod
        )
        pygame.draw.rect(screen, RED, food_rect)

        # Draw UI
        # Calculate remaining time for food to display
        time_left = max(0, (game.food_timer_limit - (pygame.time.get_ticks() - game.food_spawn_time)) // 1000)
        
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        level_text = font.render(f"Level: {game.level}", True, WHITE)
        timer_text = font.render(f"Food Timer: {time_left}s", True, YELLOW)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 100, 10))
        screen.blit(timer_text, (WIDTH // 2 - 60, 10))

        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()

if __name__ == "__main__":
    main()