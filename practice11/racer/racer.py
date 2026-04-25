import pygame, sys, random, os
from pygame.locals import *

# --- Initialization ---
pygame.init()
BASE_DIR = os.path.dirname(__file__)

def get_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

# --- Settings ---
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
INITIAL_SPEED = 5 # Starting speed for both
COIN_SCORE = 0
ENEMY_PASSED = 0 # Track how many enemies passed
N = 5 # Increase difficulty every N coins collected

# Colors
BLUE, RED, GREEN, BLACK, WHITE = (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0), (255, 255, 255)

# Fonts & Assets
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(get_path("image/Street.png"))

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# --- Classes ---

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("image/Coin.png"))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.weight = 1 # Default weight
        self.spawn()

    def spawn(self):
        """Randomly generates coin weight and prevents overlapping with enemies"""
        # Randomly choose weight: 1, 5, or 10. More '1s' makes them more common.
        self.weight = random.choice([1, 5, 10])
    
        # Adjust size based on weight
        # Weight 1 = 30x30, Weight 5 = 40x40, Weight 10 = 50x50
        size = 30 + (self.weight * 2) 
        self.image = pygame.transform.scale(pygame.image.load(get_path("image/Coin.png")), (size, size))
        self.rect = self.image.get_rect()

        # Inside spawn() after loading the image:
        if self.weight == 10:
            self.image.fill((255, 215, 0), special_flags=pygame.BLEND_RGBA_MULT) # Gold tint
        elif self.weight == 5:
            self.image.fill((192, 192, 192), special_flags=pygame.BLEND_RGBA_MULT) # Silver tint
        
        # Keep picking a new position until it doesn't overlap with an enemy
        while True:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-100, -40))
            # Check if this new rect overlaps with any sprite in the enemies group
            if not pygame.sprite.spritecollideany(self, enemies):
                break

    def move(self):
        self.rect.move_ip(0, INITIAL_SPEED) # Coins fall at general game speed
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("image/Enemy.png"))
        self.rect = self.image.get_rect()
        self.speed = INITIAL_SPEED # Enemy has its own speed variable
        self.spawn()

    def spawn(self):
        """Places enemy at top, ensuring it doesn't hit a coin immediately"""
        while True:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            if not pygame.sprite.spritecollideany(self, coins):
                break

    def move(self):
        global ENEMY_PASSED
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            ENEMY_PASSED += 1 # Count enemies avoided
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("image/Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# --- Setup Sprites ---
# 1. Create the Groups FIRST
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# 2. Create the Sprites SECOND
P1 = Player()
C1 = Coin()   # Create the coin first so the enemy can check for it
E1 = Enemy()  # Now 'coins' group exists, so E1.spawn() will work!

# 3. Add them to their groups
enemies.add(E1)
coins.add(C1)
all_sprites.add(P1, E1, C1)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 1. Background
    DISPLAYSURF.blit(background, (0,0))

    # 2. UI - Display Coin Score and Enemy Score
    scores = font_small.render(f"Enemies Passed: {ENEMY_PASSED}", True, BLACK)
    coin_txt = font_small.render(f"Score: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_txt, (SCREEN_WIDTH - 120, 10))

    # 3. Update Movements
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # 4. Check for Coin Collection
    hit_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in hit_coins:
        COIN_SCORE += coin.weight # Add the specific weight of the coin
        
        # Task: Increase speed of Enemy when player earns N coins
        if COIN_SCORE > 0 and COIN_SCORE % 2 == 0:
            E1.speed += 1 # Increase only the enemy's speed
        
        coin.spawn() # Teleport to top

    # 5. Check for Enemy Collision
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit() 
        
    pygame.display.update()
    FramePerSec.tick(FPS)