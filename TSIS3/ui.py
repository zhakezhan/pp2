import pygame
from persistence import load_leaderboard, save_settings, DIFFICULTY_PARAMS

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (180, 180, 180)
DARK_GRAY  = (60,  60,  60)
ACCENT     = (255, 200, 0)
GREEN      = (80,  200, 80)
RED_COL    = (220, 60,  60)
DARK_BG    = (18,  18,  30)
PANEL      = (30,  30,  50)
PANEL2     = (40,  40,  65)

CAR_COLORS = ["blue", "green", "red", "yellow"]
CAR_LABELS = {"blue": "Blue", "green": "Green", "red": "Red", "yellow": "Yellow"}

W, H = 400, 600


def draw_panel(surf, rect, color=PANEL, radius=12):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=radius)


def draw_button(surf, rect, text, font, hovered=False):
    color      = ACCENT  if hovered else PANEL2
    text_color = DARK_BG if hovered else WHITE
    pygame.draw.rect(surf, color, rect, border_radius=10)
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=10)
    lbl = font.render(text, True, text_color)
    surf.blit(lbl, lbl.get_rect(center=rect.center))


def gradient_bg(surf):
    for y in range(H):
        ratio = y / H
        r = int(18 + ratio * 10)
        g = int(18 + ratio * 5)
        b = int(30 + ratio * 20)
        pygame.draw.line(surf, (r, g, b), (0, y), (W, y))


def username_screen(surf, clock):
    font_title = pygame.font.SysFont("Consolas", 36, bold=True)
    font_sub   = pygame.font.SysFont("Consolas", 20)
    font_input = pygame.font.SysFont("Consolas", 28, bold=True)

    name        = ""
    btn_start   = pygame.Rect(130, 380, 140, 48)
    input_rect  = pygame.Rect(80, 280, 240, 52)

    while True:
        gradient_bg(surf)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("RACER PRO", True, ACCENT)
        surf.blit(title, title.get_rect(center=(W // 2, 120)))
        sub = font_sub.render("Enter your name to start", True, GRAY)
        surf.blit(sub, sub.get_rect(center=(W // 2, 165)))

        draw_panel(surf, input_rect.inflate(4, 4))
        name_surf = font_input.render(name + "|", True, ACCENT)
        surf.blit(name_surf, name_surf.get_rect(center=input_rect.center))

        hov = btn_start.collidepoint(mx, my)
        draw_button(surf, btn_start, "START", font_sub, hov)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()
                else:
                    if len(name) < 16:
                        name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.collidepoint(mx, my) and name.strip():
                    return name.strip()

        pygame.display.flip()
        clock.tick(60)


def main_menu(surf, clock):
    font_title = pygame.font.SysFont("Consolas", 42, bold=True)
    font_sub   = pygame.font.SysFont("Consolas", 14)
    font_btn   = pygame.font.SysFont("Consolas", 20, bold=True)

    buttons = {
        "Play":        pygame.Rect(130, 220, 140, 48),
        "Leaderboard": pygame.Rect(100, 285, 200, 48),
        "Settings":    pygame.Rect(130, 350, 140, 48),
        "Quit":        pygame.Rect(130, 415, 140, 48),
    }

    while True:
        gradient_bg(surf)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("RACER PRO", True, ACCENT)
        surf.blit(title, title.get_rect(center=(W // 2, 120)))
        sub = font_sub.render("Survive the road. Collect everything.", True, GRAY)
        surf.blit(sub, sub.get_rect(center=(W // 2, 168)))

        for label, rect in buttons.items():
            draw_button(surf, rect, label, font_btn, rect.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return label
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

        pygame.display.flip()
        clock.tick(60)


def settings_screen(surf, clock, settings):
    font_title = pygame.font.SysFont("Consolas", 32, bold=True)
    font_lbl   = pygame.font.SysFont("Consolas", 18)
    font_btn   = pygame.font.SysFont("Consolas", 17, bold=True)

    btn_back   = pygame.Rect(130, 520, 140, 44)
    btn_sound  = pygame.Rect(220, 160, 120, 38)
    btn_diff_e = pygame.Rect(60,  260, 80,  36)
    btn_diff_n = pygame.Rect(160, 260, 80,  36)
    btn_diff_h = pygame.Rect(260, 260, 80,  36)

    color_btns = {
        c: pygame.Rect(50 + i * 80, 370, 64, 36)
        for i, c in enumerate(CAR_COLORS)
    }
    COLOR_MAP = {
        "blue":   (80,  120, 255),
        "green":  (80,  200, 80),
        "red":    (220, 60,  60),
        "yellow": (255, 220, 40),
    }

    while True:
        gradient_bg(surf)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("SETTINGS", True, ACCENT)
        surf.blit(title, title.get_rect(center=(W // 2, 80)))

        # Sound toggle
        surf.blit(font_lbl.render("Sound:", True, WHITE), (60, 168))
        sound_label = "ON" if settings["sound"] else "OFF"
        sound_col   = GREEN if settings["sound"] else RED_COL
        pygame.draw.rect(surf, sound_col, btn_sound, border_radius=8)
        lbl_s = font_btn.render(sound_label, True, WHITE)
        surf.blit(lbl_s, lbl_s.get_rect(center=btn_sound.center))

        # Difficulty buttons
        surf.blit(font_lbl.render("Difficulty:", True, WHITE), (60, 230))
        for rect, diff in [(btn_diff_e, "easy"), (btn_diff_n, "normal"), (btn_diff_h, "hard")]:
            active     = settings["difficulty"] == diff
            bg_color   = ACCENT if active else PANEL2
            txt_color  = DARK_BG if active else WHITE   # FIX: was always WHITE
            pygame.draw.rect(surf, bg_color, rect, border_radius=8)
            pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=8)
            lbl = font_btn.render(diff.capitalize(), True, txt_color)
            surf.blit(lbl, lbl.get_rect(center=rect.center))

        # Car colour buttons
        surf.blit(font_lbl.render("Car Color:", True, WHITE), (60, 330))
        for color, rect in color_btns.items():
            active = settings["car_color"] == color
            pygame.draw.rect(surf, COLOR_MAP[color], rect, border_radius=8)
            if active:
                pygame.draw.rect(surf, ACCENT, rect, 3, border_radius=8)
            lbl = font_btn.render(CAR_LABELS[color], True, WHITE)
            surf.blit(lbl, lbl.get_rect(center=rect.center))

        # Difficulty description hint
        diff_hints = {
            "easy":   "Easy: slow, sparse",
            "normal": "Normal: balanced",
            "hard":   "Hard: fast & dense",
        }
        hint = font_lbl.render(diff_hints[settings["difficulty"]], True, GRAY)
        surf.blit(hint, hint.get_rect(center=(W // 2, 310)))

        draw_button(surf, btn_back, "Back", font_btn, btn_back.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_sound.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                for rect, diff in [(btn_diff_e, "easy"), (btn_diff_n, "normal"), (btn_diff_h, "hard")]:
                    if rect.collidepoint(mx, my):
                        settings["difficulty"] = diff
                        save_settings(settings)
                for color, rect in color_btns.items():
                    if rect.collidepoint(mx, my):
                        settings["car_color"] = color
                        save_settings(settings)
                if btn_back.collidepoint(mx, my):
                    return

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen(surf, clock):
    font_title = pygame.font.SysFont("Consolas", 30, bold=True)
    font_row   = pygame.font.SysFont("Consolas", 16)
    font_hdr   = pygame.font.SysFont("Consolas", 15, bold=True)
    font_btn   = pygame.font.SysFont("Consolas", 18, bold=True)
    btn_back   = pygame.Rect(130, 540, 140, 44)

    while True:
        gradient_bg(surf)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("LEADERBOARD", True, ACCENT)
        surf.blit(title, title.get_rect(center=(W // 2, 55)))

        board = load_leaderboard()

        # Header
        header = font_hdr.render(
            f"{'#':<3} {'Name':<13} {'Score':>6}  {'Dist':>6}  {'Coins':>5}", True, ACCENT
        )
        surf.blit(header, (30, 95))
        pygame.draw.line(surf, ACCENT, (30, 115), (370, 115), 1)

        if not board:
            empty = font_row.render("No scores yet — play a game!", True, GRAY)
            surf.blit(empty, empty.get_rect(center=(W // 2, 300)))
        else:
            for i, entry in enumerate(board):
                if i == 0:
                    color = ACCENT
                elif i < 3:
                    color = GRAY
                else:
                    color = WHITE
                row = font_row.render(
                    f"{i+1:<3} {entry['name'][:12]:<13} "
                    f"{entry['score']:>6}  {int(entry['distance']):>5}m  {entry['coins']:>5}",
                    True, color
                )
                surf.blit(row, (30, 125 + i * 36))

        draw_button(surf, btn_back, "Back", font_btn, btn_back.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(mx, my):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(surf, clock, score, distance, coins):
    font_title = pygame.font.SysFont("Consolas", 38, bold=True)
    font_stat  = pygame.font.SysFont("Consolas", 20)
    font_btn   = pygame.font.SysFont("Consolas", 18, bold=True)
    font_hint  = pygame.font.SysFont("Consolas", 13)

    btn_retry = pygame.Rect(60,  450, 120, 46)
    btn_menu  = pygame.Rect(220, 450, 120, 46)

    while True:
        gradient_bg(surf)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("GAME OVER", True, RED_COL)
        surf.blit(title, title.get_rect(center=(W // 2, 150)))

        panel = pygame.Rect(70, 210, 260, 210)
        draw_panel(surf, panel)

        stats = [
            ("Score",    str(score)),
            ("Distance", f"{int(distance)} m"),
            ("Coins",    str(coins)),
            ("Final",    f"{score} pts"),
        ]
        for i, (label, val) in enumerate(stats):
            lbl   = font_stat.render(f"{label}:", True, GRAY)
            val_s = font_stat.render(val, True, ACCENT)
            surf.blit(lbl,   (100, 228 + i * 44))
            surf.blit(val_s, val_s.get_rect(right=310, top=228 + i * 44))

        draw_button(surf, btn_retry, "Retry", font_btn, btn_retry.collidepoint(mx, my))
        draw_button(surf, btn_menu,  "Menu",  font_btn, btn_menu.collidepoint(mx, my))

        hint = font_hint.render("ESC = Menu", True, GRAY)
        surf.blit(hint, hint.get_rect(center=(W // 2, 510)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_r:
                    return "retry"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(mx, my):
                    return "retry"
                if btn_menu.collidepoint(mx, my):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)