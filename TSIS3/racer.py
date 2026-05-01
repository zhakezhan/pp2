import pygame
import random
from persistence import DIFFICULTY_PARAMS

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 0,   0)
YELLOW = (255, 220, 40)
ORANGE = (255, 140, 0)
GREEN  = (80,  200, 80)
CYAN   = (0,   220, 220)
GRAY   = (160, 160, 160)
DARK   = (18,  18,  30)
ACCENT = (255, 200, 0)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
ROAD_LEFT     = 40
ROAD_RIGHT    = 360
LANE_COUNT    = 4
LANE_W        = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT
LANES         = [ROAD_LEFT + LANE_W * i + LANE_W // 2 for i in range(LANE_COUNT)]

POWERUP_TYPES    = ["nitro", "shield", "repair"]
POWERUP_COLORS   = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
POWERUP_DURATION = {"nitro": 4000, "shield": 0, "repair": 0}
POWERUP_LABELS   = {"nitro": "NITRO", "shield": "SHIELD", "repair": "REPAIR"}

OBSTACLE_TYPES = ["oil", "barrier", "pothole"]
OBSTACLE_COLORS = {
    "oil":     (30,  30,  30),
    "barrier": (220, 60,  60),
    "pothole": (80,  50,  20),
}

CAR_IMAGE_MAP = {
    "blue":   "assets/images/Player_bl.png",
    "green":  "assets/images/Player_gr.png",
    "red":    "assets/images/Player_red.png",
    "yellow": "assets/images/Player_yel.png",
}


class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="blue"):
        super().__init__()
        path = CAR_IMAGE_MAP.get(car_color, CAR_IMAGE_MAP["blue"])
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except Exception:
            self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
            COLOR_MAP = {
                "blue":   (80,  120, 255),
                "green":  (80,  200, 80),
                "red":    (220, 60,  60),
                "yellow": (255, 220, 40),
            }
            col = COLOR_MAP.get(car_color, (80, 120, 255))
            pygame.draw.rect(self.image, col, (0, 0, 40, 70), border_radius=8)
            pygame.draw.rect(self.image, (180, 220, 255), (6, 8, 28, 16), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (0, 12, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (32, 12, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (0, 46, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (32, 46, 8, 14), border_radius=3)
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.shield_active = False
        self.nitro_active  = False
        self.nitro_end     = 0

    def move(self):
        keys = pygame.key.get_pressed()
        speed = 7 if self.nitro_active else 5
        if self.rect.left > ROAD_LEFT and keys[pygame.K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if self.rect.right < ROAD_RIGHT and keys[pygame.K_RIGHT]:
            self.rect.move_ip(speed, 0)

    def update_powerups(self, now):
        if self.nitro_active and now >= self.nitro_end:
            self.nitro_active = False

    def activate_nitro(self, now, duration=4000):
        self.nitro_active = True
        self.nitro_end = now + duration

    def activate_shield(self):
        self.shield_active = True

    def draw_shield(self, surf):
        if self.shield_active:
            # Use SRCALPHA surface to avoid color-tuple crash
            shield_surf = pygame.Surface(
                (self.rect.width + 24, self.rect.height + 24), pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                shield_surf, (0, 220, 220, 80),
                (0, 0, shield_surf.get_width(), shield_surf.get_height())
            )
            pygame.draw.ellipse(
                shield_surf, (0, 220, 220, 220),
                (0, 0, shield_surf.get_width(), shield_surf.get_height()), 2
            )
            surf.blit(shield_surf, (self.rect.x - 12, self.rect.y - 12))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/Enemy.png").convert_alpha()
        except Exception:
            self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (220, 60, 60), (0, 0, 40, 70), border_radius=8)
            pygame.draw.rect(self.image, (180, 220, 255), (6, 42, 28, 16), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (0, 10, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (32, 10, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (0, 44, 8, 14), border_radius=3)
            pygame.draw.rect(self.image, BLACK, (32, 44, 8, 14), border_radius=3)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = (random.choice(LANES), -80)

    def move(self):
        self.rect.move_ip(0, self.speed)

    def respawn(self, speed, player_rect=None):
        self.speed = speed
        x = safe_spawn_x(player_rect) if player_rect else random.choice(LANES)
        self.rect.center = (x, random.randint(-400, -80))


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/images/Coin.png").convert_alpha()
        except Exception:
            self.original_image = None
        self.speed = speed
        self.spawn()

    def spawn(self, all_groups=None):
        self.weight = random.choice([1, 3, 5])
        size = 20 + self.weight * 5
        if self.original_image:
            self.image = pygame.transform.scale(self.original_image, (size, size))
        else:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (size // 2, size // 2), size // 2)
            pygame.draw.circle(self.image, (200, 160, 0), (size // 2, size // 2), size // 2, 2)
        # Try up to 10 times to find a clear lane
        groups = all_groups or []
        for _ in range(10):
            lx = random.choice(LANES)
            y  = -50
            if lane_clear(lx, y, groups, min_gap_y=80):
                break
        self.rect = self.image.get_rect(center=(lx, y))

    def move(self, all_groups=None):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn(all_groups=all_groups)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed      = speed
        self.kind       = random.choice(POWERUP_TYPES)
        self.color      = POWERUP_COLORS[self.kind]
        self.image      = pygame.Surface((36, 36), pygame.SRCALPHA)
        self.spawn_time = pygame.time.get_ticks()
        self._draw()
        self.rect = self.image.get_rect(center=(random.choice(LANES), -60))

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (18, 18), 17)
        pygame.draw.circle(self.image, WHITE, (18, 18), 17, 2)
        font = pygame.font.SysFont("Consolas", 9, bold=True)
        lbl = font.render(POWERUP_LABELS[self.kind][:3], True, WHITE)
        self.image.blit(lbl, lbl.get_rect(center=(18, 18)))

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self, now, timeout=8000):
        return now - self.spawn_time > timeout or self.rect.top > SCREEN_HEIGHT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind  = random.choice(OBSTACLE_TYPES)
        self.speed = speed
        if self.kind == "oil":
            self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (*OBSTACLE_COLORS["oil"], 200), (0, 0, 50, 30))
            pygame.draw.ellipse(self.image, (60, 0, 80, 120), (8, 6, 20, 10))
        elif self.kind == "barrier":
            self.image = pygame.Surface((60, 18), pygame.SRCALPHA)
            pygame.draw.rect(self.image, OBSTACLE_COLORS["barrier"], (0, 0, 60, 18), border_radius=4)
            pygame.draw.rect(self.image, WHITE, (0, 0, 60, 18), 2, border_radius=4)
            for x in range(5, 55, 12):
                pygame.draw.rect(self.image, WHITE, (x, 4, 6, 10))
        else:  # pothole
            self.image = pygame.Surface((34, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, OBSTACLE_COLORS["pothole"], (0, 0, 34, 20))
            pygame.draw.ellipse(self.image, (50, 30, 10), (4, 4, 26, 12))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -40))

    def move(self):
        self.rect.move_ip(0, self.speed)


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((ROAD_RIGHT - ROAD_LEFT, 14), pygame.SRCALPHA)
        for x in range(0, self.image.get_width(), 20):
            pygame.draw.rect(self.image, (*ORANGE, 180), (x, 0, 14, 14), border_radius=3)
        self.rect = self.image.get_rect(topleft=(ROAD_LEFT, -20))

    def move(self):
        self.rect.move_ip(0, self.speed)


def safe_spawn_x(player_rect, exclude=None):
    """Return a lane x-centre avoiding the player's current lane.
    All 4 lanes are eligible; only the one the player occupies is excluded.
    Falls back to any lane if all are excluded.
    """
    player_lane = min(LANES, key=lambda lx: abs(lx - player_rect.centerx))
    excluded = {player_lane}
    if exclude:
        excluded.update(exclude)
    choices = [lx for lx in LANES if lx not in excluded]
    return random.choice(choices) if choices else random.choice(LANES)


def pick_lane_spread(n, player_rect):
    """Pick n distinct lanes spread across the road, avoiding player's lane."""
    player_lane = min(LANES, key=lambda lx: abs(lx - player_rect.centerx))
    available   = [lx for lx in LANES if lx != player_lane]
    random.shuffle(available)
    pool = available if n <= len(available) else LANES[:]
    return pool[:n]


def lane_clear(lane_x, y_top, all_groups, min_gap_y=100, min_gap_x=None):
    """Return True if no sprite in any group overlaps the spawn point.
    Checks same-lane sprites only (within min_gap_x) for vertical gap.
    """
    if min_gap_x is None:
        min_gap_x = LANE_W - 5
    for group in all_groups:
        for sprite in group:
            if abs(sprite.rect.centerx - lane_x) < min_gap_x:
                if sprite.rect.bottom > y_top - min_gap_y:
                    return False
    return True


def run_game(surf, clock, username, settings):
    pygame.display.set_caption("Racer Pro")

    diff       = settings.get("difficulty", "normal")
    params     = DIFFICULTY_PARAMS[diff]
    SPEED      = params["speed"]
    SPAWN_RATE = params["spawn_rate"]
    SPEED_STEP = params["speed_step"]

    sound_on    = settings.get("sound", True)
    crash_sound = None
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        if sound_on:
            pygame.mixer.music.load("assets/sounds/background.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            crash_sound = pygame.mixer.Sound("assets/sounds/crash.wav")
            crash_sound.set_volume(0.7)
    except Exception as e:
        print(f"[Sound error] {e}")
        crash_sound = None

    # Background
    try:
        background = pygame.image.load("assets/images/AnimatedStreet.png").convert()
        use_bg_image = True
    except Exception:
        background    = None
        use_bg_image  = False

    def draw_bg(y1, y2):
        if use_bg_image:
            surf.blit(background, (0, int(y1)))
            surf.blit(background, (0, int(y2)))
        else:
            surf.fill((45, 45, 55))
            # Road surface
            pygame.draw.rect(surf, (60, 60, 65),
                             (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
            # Scrolling dashed lane dividers
            dash_h, gap_h = 30, 20
            period = dash_h + gap_h
            offset = int(y1) % period
            for li in range(1, LANE_COUNT):
                x = ROAD_LEFT + LANE_W * li
                y = -period + offset
                while y < SCREEN_HEIGHT:
                    pygame.draw.rect(surf, (180, 180, 100), (x - 1, y, 2, dash_h))
                    y += period
            # Road edge lines
            pygame.draw.rect(surf, (220, 200, 50), (ROAD_LEFT - 3, 0, 3, SCREEN_HEIGHT))
            pygame.draw.rect(surf, (220, 200, 50), (ROAD_RIGHT, 0, 3, SCREEN_HEIGHT))

    bg_y1, bg_y2 = 0, -SCREEN_HEIGHT

    font_sm  = pygame.font.SysFont("Consolas", 16, bold=True)
    font_med = pygame.font.SysFont("Consolas", 19, bold=True)

    P1 = Player(settings.get("car_color", "blue"))

    enemies   = pygame.sprite.Group()
    coins     = pygame.sprite.Group()
    powerups  = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    strips    = pygame.sprite.Group()

    # Initial enemies — spread across distinct lanes, staggered vertically
    for i, lx in enumerate(pick_lane_spread(2, P1.rect)):
        e = Enemy(SPEED)
        e.rect.centerx = lx
        e.rect.centery = -150 - i * 200   # stagger so they don't cluster
        enemies.add(e)

    coins.add(Coin(SPEED))

    SCORE      = 0
    COIN_SCORE = 0
    distance   = 0.0
    TOTAL_DIST = 3000.0

    spawn_timer   = 0
    powerup_timer = 0
    strip_timer   = 0

    # Target number of active enemies — grows with distance
    TARGET_ENEMIES = 2

    # Only one power-up active at a time
    active_powerup_kind = None
    active_powerup_end  = 0

    # Minimum gap (in pixels) required between a new enemy and any existing enemy
    MIN_GAP = 90

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    running = True
    while running:
        now = pygame.time.get_ticks()

        #  Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:        # FIX: was event.type == pygame.K_ESCAPE
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == INC_SPEED:
                SPEED = round(SPEED + 0.3, 1)

        #  Background 
        bg_y1 += SPEED * 0.8
        bg_y2 += SPEED * 0.8
        if bg_y1 >= SCREEN_HEIGHT:
            bg_y1 = -SCREEN_HEIGHT
        if bg_y2 >= SCREEN_HEIGHT:
            bg_y2 = -SCREEN_HEIGHT
        draw_bg(bg_y1, bg_y2)

        distance += SPEED * 0.05

        #  Update
        P1.move()
        P1.update_powerups(now)

        for e in list(enemies):
            e.move()
            if e.rect.top > SCREEN_HEIGHT:
                SCORE += 1
                e.kill()   # pool logic will respawn up to TARGET_ENEMIES next tick

        for c in list(coins):
            c.speed = SPEED
            c.move(all_groups=[enemies, obstacles, coins])

        for obs in list(obstacles):
            obs.speed = SPEED
            obs.move()
            if obs.rect.top > SCREEN_HEIGHT:
                obs.kill()

        for pu in list(powerups):
            pu.speed = SPEED
            pu.move()
            if pu.expired(now):
                pu.kill()

        for st in list(strips):
            st.speed = SPEED
            st.move()
            if st.rect.top > SCREEN_HEIGHT:
                st.kill()

        #  Difficulty scaling: update target enemy count 
        TARGET_ENEMIES = min(2 + int(distance // 600), LANE_COUNT)

        #  Spawning 
        spawn_timer += 1
        if spawn_timer >= SPAWN_RATE:
            spawn_timer = 0

            # Kill surplus enemies so count never exceeds target
            current = list(enemies)
            while len(current) > TARGET_ENEMIES:
                current.pop().kill()
                current = list(enemies)

            # Spawn enemies up to the target, one per tick, with gap check
            if len(enemies) < TARGET_ENEMIES:
                occupied_lanes = {
                    min(LANES, key=lambda lx: abs(lx - e.rect.centerx))
                    for e in enemies
                    if e.rect.top < 0
                }
                free_lanes = [lx for lx in LANES if lx not in occupied_lanes]
                if not free_lanes:
                    free_lanes = LANES[:]

                random.shuffle(free_lanes)
                for candidate in free_lanes:
                    if lane_clear(candidate, -80, [enemies, obstacles, coins, powerups]):
                        e = Enemy(SPEED)
                        e.rect.centerx = candidate
                        e.rect.top = -80
                        enemies.add(e)
                        break

            # Obstacle — check all groups before spawning
            if random.random() < 0.45 and len(obstacles) < 3:
                shuffled = LANES[:]
                random.shuffle(shuffled)
                for lx in shuffled:
                    if lane_clear(lx, -40, [enemies, obstacles, coins, powerups], min_gap_y=90):
                        obs = Obstacle(SPEED)
                        obs.rect.centerx = lx
                        obs.rect.top = -40
                        obstacles.add(obs)
                        break

        # Power-up — one on screen at a time
        powerup_timer += 1
        if powerup_timer >= 180:
            powerup_timer = 0
            if random.random() < 0.45 and len(powerups) == 0:
                shuffled = LANES[:]
                random.shuffle(shuffled)
                for lx in shuffled:
                    if lane_clear(lx, -60, [enemies, obstacles, coins, powerups], min_gap_y=90):
                        pu = PowerUp(SPEED)
                        pu.rect.centerx = lx
                        powerups.add(pu)
                        break

        # Nitro strip road event
        strip_timer += 1
        if strip_timer >= 300:
            strip_timer = 0
            if random.random() < 0.3:
                strips.add(NitroStrip(SPEED))

        #  Coin collection ─
        for c in pygame.sprite.spritecollide(P1, coins, False):
            old = COIN_SCORE
            COIN_SCORE += c.weight
            if (COIN_SCORE // SPEED_STEP) > (old // SPEED_STEP):
                SPEED = round(SPEED + 0.5, 1)
            c.spawn(all_groups=[enemies, obstacles, coins])

        #  Power-up collection — only one active at a time ─
        for pu in pygame.sprite.spritecollide(P1, powerups, True):
            already_active = (
                (active_powerup_kind == "nitro"  and P1.nitro_active) or
                (active_powerup_kind == "shield" and P1.shield_active) or
                (active_powerup_kind == "repair" and now < active_powerup_end)
            )
            if not already_active:
                active_powerup_kind = pu.kind
                if pu.kind == "nitro":
                    P1.activate_nitro(now, POWERUP_DURATION["nitro"])
                    active_powerup_end = now + POWERUP_DURATION["nitro"]
                elif pu.kind == "shield":
                    P1.activate_shield()
                    active_powerup_end = now + 999999
                elif pu.kind == "repair":
                    # FIX: actually clears all obstacles currently on screen
                    obstacles.empty()
                    active_powerup_end = now + 2000

        #  Nitro strip 
        if pygame.sprite.spritecollide(P1, strips, False) and not P1.nitro_active:
            P1.activate_nitro(now, 2000)
            active_powerup_kind = "nitro"
            active_powerup_end  = now + 2000

        #  Obstacle collision 
        obs_hit = pygame.sprite.spritecollide(P1, obstacles, False)
        if obs_hit:
            if P1.shield_active:
                P1.shield_active = False
                active_powerup_kind = None
                for o in obs_hit:
                    o.kill()
            else:
                pygame.mixer.music.stop()
                if crash_sound:
                    crash_sound.play()
                running = False

        #  Enemy collision 
        enemy_hit = pygame.sprite.spritecollide(P1, enemies, False)
        if enemy_hit:
            if P1.shield_active:
                P1.shield_active = False
                active_powerup_kind = None
                for e in enemy_hit:
                    e.kill()
            else:
                pygame.mixer.music.stop()
                if crash_sound:
                    crash_sound.play()
                running = False

        if not running:
            break

        #  Draw
        for st in strips:
            surf.blit(st.image, st.rect)
        for obs in obstacles:
            surf.blit(obs.image, obs.rect)
        for c in coins:
            surf.blit(c.image, c.rect)
        for pu in powerups:
            surf.blit(pu.image, pu.rect)
        for e in enemies:
            surf.blit(e.image, e.rect)
        surf.blit(P1.image, P1.rect)
        P1.draw_shield(surf)

        #  HUD
        hud_bg = pygame.Surface((SCREEN_WIDTH, 62), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 170))
        surf.blit(hud_bg, (0, 0))

        surf.blit(font_sm.render(f"Score:  {SCORE}",      True, WHITE),  (8,  4))
        surf.blit(font_sm.render(f"Coins:  {COIN_SCORE}", True, YELLOW), (8, 22))
        surf.blit(font_sm.render(f"Speed:  {SPEED:.1f}",  True, ACCENT), (8, 40))
        surf.blit(font_sm.render(
            f"Dist: {int(distance)}/{int(TOTAL_DIST)}m", True, GRAY), (215, 4))
        surf.blit(font_sm.render(f"Player: {username}",   True, GRAY),   (215, 22))

        bar_w = int(min(distance / TOTAL_DIST, 1.0) * 150)
        pygame.draw.rect(surf, DARK,  (215, 44, 150, 10), border_radius=4)
        pygame.draw.rect(surf, GREEN, (215, 44, bar_w,  10), border_radius=4)
        pygame.draw.rect(surf, GRAY,  (215, 44, 150, 10), 1, border_radius=4)

        # Active power-up banner
        if active_powerup_kind:
            remaining = max(0, active_powerup_end - now)
            label = None
            col   = WHITE
            if active_powerup_kind == "nitro" and P1.nitro_active:
                label = f"NITRO {remaining // 1000 + 1}s"
                col   = ORANGE
            elif active_powerup_kind == "shield" and P1.shield_active:
                label = "SHIELD ACTIVE"
                col   = CYAN
            elif active_powerup_kind == "repair" and remaining > 0:
                label = "REPAIR!"
                col   = GREEN
            else:
                active_powerup_kind = None   # expired — clear

            if label:
                pw_w = 148
                pw_surf = pygame.Surface((pw_w, 26), pygame.SRCALPHA)
                pw_surf.fill((0, 0, 0, 150))
                surf.blit(pw_surf, (SCREEN_WIDTH // 2 - pw_w // 2, 64))
                pw_lbl = font_med.render(label, True, col)
                surf.blit(pw_lbl, pw_lbl.get_rect(center=(SCREEN_WIDTH // 2, 77)))

        pygame.display.flip()
        clock.tick(60)

    # Wait for crash sound to finish playing, then stop everything
    if crash_sound:
        pygame.time.wait(int(crash_sound.get_length() * 1000))
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

    final_score = SCORE * 10 + COIN_SCORE * 5 + int(distance)
    return final_score, distance, COIN_SCORE