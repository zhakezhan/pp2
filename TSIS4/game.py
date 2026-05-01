import pygame
import random
import time
import json
from config import *
from db import get_personal_best, save_session


def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except Exception:
        return {"snake_color": list(GREEN), "grid": True, "sound": True}


def _random_cell(blocked):
    while True:
        pos = [
            random.randrange(1, GRID_COLS - 1) * BLOCK_SIZE,
            random.randrange(1, GRID_ROWS - 1) * BLOCK_SIZE,
        ]
        if pos not in blocked:
            return pos


def _gradient_bg(surf):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(14 + t * 6)
        g = int(14 + t * 4)
        b = int(24 + t * 14)
        pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))


class SnakeGame:
    def __init__(self, player_id, settings):
        self.player_id = player_id
        self.settings  = settings
        self.snake_color = tuple(settings.get("snake_color", list(GREEN)))

        self.snake     = [[200, 300], [180, 300], [160, 300]]
        self.direction = "RIGHT"
        self.next_dir  = "RIGHT"

        self.score = 0
        self.level = 1
        self.speed = FPS_BASE

        self.food_pos        = None
        self.food_weight     = 1
        self.food_spawn_time = 0

        self.poison_pos        = None
        self.poison_spawn_time = 0

        self.powerup_pos       = None
        self.powerup_kind      = None
        self.powerup_spawn_time = 0

        self.active_powerup      = None
        self.active_powerup_end  = 0
        self.shield_active       = False

        self.obstacles = []

        self.personal_best = get_personal_best(player_id)

        self.spawn_food()
        self._maybe_spawn_poison()

    def _blocked_cells(self):
        return self.snake + self.obstacles + [
            p for p in [self.food_pos, self.poison_pos, self.powerup_pos] if p
        ]

    def spawn_food(self):
        self.food_pos    = _random_cell(self._blocked_cells())
        self.food_weight = random.randint(1, 3)
        self.food_spawn_time = pygame.time.get_ticks()

    def _maybe_spawn_poison(self):
        if random.random() < 0.4:
            self.poison_pos = _random_cell(self._blocked_cells())
            self.poison_spawn_time = pygame.time.get_ticks()
        else:
            self.poison_pos = None

    def _spawn_powerup(self):
        if self.powerup_pos is not None:
            return
        self.powerup_kind      = random.choice(["speed", "slow", "shield"])
        self.powerup_pos       = _random_cell(self._blocked_cells())
        self.powerup_spawn_time = pygame.time.get_ticks()

    def _spawn_obstacles(self):
        if self.level < 3:
            return
        count = OBSTACLE_PER_LEVEL * (self.level - 2)
        head  = self.snake[0]
        self.obstacles = []
        attempts = 0
        while len(self.obstacles) < count and attempts < 500:
            attempts += 1
            pos = _random_cell(self.snake + self.obstacles + [
                p for p in [self.food_pos, self.poison_pos] if p
            ])
            if abs(pos[0] - head[0]) < BLOCK_SIZE * 3 and abs(pos[1] - head[1]) < BLOCK_SIZE * 3:
                continue
            self.obstacles.append(pos)

    def handle_key(self, key):
        if key == pygame.K_UP    and self.direction != "DOWN":  self.next_dir = "UP"
        elif key == pygame.K_DOWN  and self.direction != "UP":   self.next_dir = "DOWN"
        elif key == pygame.K_LEFT  and self.direction != "RIGHT": self.next_dir = "LEFT"
        elif key == pygame.K_RIGHT and self.direction != "LEFT":  self.next_dir = "RIGHT"

    def update(self):
        now = pygame.time.get_ticks()
        self.direction = self.next_dir

        if now - self.food_spawn_time > FOOD_TIMER_LIMIT:
            self.spawn_food()

        if self.poison_pos and now - self.poison_spawn_time > FOOD_TIMER_LIMIT + 2000:
            self._maybe_spawn_poison()

        if self.powerup_pos and now - self.powerup_spawn_time > POWERUP_LIFETIME:
            self.powerup_pos  = None
            self.powerup_kind = None

        if self.active_powerup in ("speed", "slow") and now > self.active_powerup_end:
            self.speed = FPS_BASE + (self.level - 1) * 2
            self.active_powerup = None

        if random.random() < 0.008 and self.powerup_pos is None:
            self._spawn_powerup()

        head = list(self.snake[0])
        if self.direction == "UP":    head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":  head[1] += BLOCK_SIZE
        elif self.direction == "LEFT":  head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE

        hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
        hit_self = head in self.snake
        hit_obs  = head in self.obstacles

        if hit_wall or hit_self or hit_obs:
            if self.shield_active:
                self.shield_active = False
                self.active_powerup = None
                if hit_wall:
                # телепорт на противоположную сторону
                    if head[0] < 0:
                        head[0] = WIDTH - BLOCK_SIZE
                    elif head[0] >= WIDTH:
                        head[0] = 0
                    if head[1] < 0:
                        head[1] = HEIGHT - BLOCK_SIZE
                    elif head[1] >= HEIGHT:
                        head[1] = 0
            else:
                return False

        self.snake.insert(0, head)

        if head == self.food_pos:
            old_score  = self.score
            self.score += self.food_weight
            if self.score // LEVEL_UP_EVERY > old_score // LEVEL_UP_EVERY:
                self.level += 1
                self.speed  = FPS_BASE + (self.level - 1) * 2
                self._spawn_obstacles()
            self.spawn_food()
            self._maybe_spawn_poison()

        elif self.poison_pos and head == self.poison_pos:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.poison_pos = None
            self._maybe_spawn_poison()
            if len(self.snake) <= 1:
                return False

        elif self.powerup_pos and head == self.powerup_pos:
            kind = self.powerup_kind
            self.active_powerup     = kind
            self.active_powerup_end = now + POWERUP_DURATION
            if kind == "speed":
                self.speed = min(self.speed + 4, 24)
            elif kind == "slow":
                self.speed = max(self.speed - 3, 4)
            elif kind == "shield":
                self.shield_active  = True
                self.active_powerup = "shield"
            self.powerup_pos  = None
            self.powerup_kind = None

        else:
            self.snake.pop()

        return True

    def draw(self, surf):
        _gradient_bg(surf)

        if self.settings.get("grid", True):
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(surf, (22, 22, 36), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(surf, (22, 22, 36), (0, y), (WIDTH, y))

        for obs in self.obstacles:
            pygame.draw.rect(surf, LIGHT_GRAY, (obs[0]+1, obs[1]+1, BLOCK_SIZE-2, BLOCK_SIZE-2), border_radius=3)
            pygame.draw.rect(surf, WHITE,      (obs[0]+1, obs[1]+1, BLOCK_SIZE-2, BLOCK_SIZE-2), 1, border_radius=3)

        for i, block in enumerate(self.snake):
            color = self.snake_color if i > 0 else tuple(min(255, c + 60) for c in self.snake_color)
            pygame.draw.rect(surf, color, (block[0]+1, block[1]+1, BLOCK_SIZE-2, BLOCK_SIZE-2), border_radius=4)

        if self.shield_active:
            h = self.snake[0]
            pygame.draw.rect(surf, (*ACCENT, 120), (h[0]-2, h[1]-2, BLOCK_SIZE+4, BLOCK_SIZE+4), 2, border_radius=6)

        if self.food_pos:
            fw = self.food_weight
            col = FOOD_COLORS[fw]
            fs = fw * 5 + 8
            fx = self.food_pos[0] + (BLOCK_SIZE - fs) // 2
            fy = self.food_pos[1] + (BLOCK_SIZE - fs) // 2
            pygame.draw.rect(surf, col, (fx, fy, fs, fs), border_radius=4)

        if self.poison_pos:
            px = self.poison_pos[0] + 4
            py = self.poison_pos[1] + 4
            ps = BLOCK_SIZE - 8
            pygame.draw.rect(surf, POISON_COLOR, (px, py, ps, ps), border_radius=4)
            pygame.draw.rect(surf, RED, (px, py, ps, ps), 1, border_radius=4)

        if self.powerup_pos and self.powerup_kind:
            col = POWERUP_COLOR[self.powerup_kind]
            cx  = self.powerup_pos[0] + BLOCK_SIZE // 2
            cy  = self.powerup_pos[1] + BLOCK_SIZE // 2
            pygame.draw.circle(surf, col, (cx, cy), BLOCK_SIZE // 2 - 1)
            pygame.draw.circle(surf, WHITE, (cx, cy), BLOCK_SIZE // 2 - 1, 1)

        self._draw_hud(surf)

    def _draw_hud(self, surf):
        font_sm = pygame.font.SysFont("Consolas", 16, bold=True)
        font_md = pygame.font.SysFont("Consolas", 18, bold=True)
        now = pygame.time.get_ticks()

        hud = pygame.Surface((WIDTH, 52), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 170))
        surf.blit(hud, (0, 0))

        surf.blit(font_sm.render(f"Score:  {self.score}",  True, WHITE),  (10, 6))
        surf.blit(font_sm.render(f"Level:  {self.level}",  True, ACCENT), (10, 28))
        surf.blit(font_sm.render(f"Best:   {self.personal_best}", True, LIGHT_GRAY), (170, 6))

        time_left = max(0, (FOOD_TIMER_LIMIT - (now - self.food_spawn_time)) // 1000)
        surf.blit(font_sm.render(f"Food:  {time_left}s", True, FOOD_COLORS[self.food_weight]), (170, 28))

        if self.active_powerup:
            if self.active_powerup == "shield":
                pu_txt = "SHIELD active"
                col = ACCENT
            else:
                rem = max(0, (self.active_powerup_end - now) // 1000)
                pu_txt = f"{self.active_powerup.upper()} {rem}s"
                col = POWERUP_COLOR.get(self.active_powerup, WHITE)
            lbl = font_md.render(pu_txt, True, col)
            surf.blit(lbl, lbl.get_rect(center=(WIDTH // 2, 70)))

    def finish(self):
        save_session(self.player_id, self.score, self.level)