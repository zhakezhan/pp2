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
SPEED = 5
SCORE = 0
COIN_SCORE = 0

# Colors
BLUE, RED, GREEN, BLACK, WHITE = (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0), (255, 255, 255)

# Fonts & Assets
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(get_path("ins/images/Street.png"))
crash_sound = pygame.mixer.Sound(get_path("ins/sounds/crash.wav"))
pygame.mixer.music.load(get_path("ins/sounds/background.wav"))
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound(get_path("ins/sounds/coin_sound.wav"))

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# --- Classes ---
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load coin image - ensure "Coin.png" exists in your folder
        self.image = pygame.image.load(get_path("ins/images/Coin.png"))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        """Places the coin at a random position at the top"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        # If coin leaves screen without being collected, reset it
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()
    def reset(self):
        """
        Used when the player collects the coin. 
        Instantly moves it back to the top.
        """
        self.spawn()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("ins/images/Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_path("ins/images/Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# --- Setup Sprites ---
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Timer for Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
      
    # Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 1. Draw the Background first
    DISPLAYSURF.blit(background, (0,0))

    # 2. Render and draw scores
    # Top Left: Enemy Score
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Top Right: Coin Score
    # We use (SCREEN_WIDTH - 100) to keep it on the right side
    coin_scores = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(coin_scores, (SCREEN_WIDTH - 100, 10))

    # 3. Move and Re-draw all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # 4. Check for Coin Collection
    # This checks if the Player (P1) hits any sprite in the 'coins' group
    if pygame.sprite.spritecollide(P1, coins, False):
        COIN_SCORE += 1
        coin_sound.play()
        C1.spawn() # Teleports the coin back to the top

    # 5. Check for Enemy Collision
    if pygame.sprite.spritecollideany(P1, enemies):
        # Optional: stop the music so the crash sound is clearer
        pygame.mixer.music.stop()
        crash_sound.play()
        
        # Game Over Screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        
        # Display final results
        final_stat = font_small.render(f"Final Coins: {COIN_SCORE}", True, WHITE)
        DISPLAYSURF.blit(final_stat, (130, 320))
        
        pygame.display.update()
        
        # Pause briefly before closing
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)