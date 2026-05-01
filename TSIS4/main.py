import pygame
import sys
import json
import random
from config import *
from db import init_db, get_or_create_player, get_leaderboard
from game import SnakeGame, load_settings, _gradient_bg


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro — TSIS 4")
clock = pygame.time.Clock()


def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=2)


def draw_panel(surf, rect, radius=12):
    pygame.draw.rect(surf, PANEL, rect, border_radius=radius)
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=radius)


def draw_button(surf, rect, text, font, hovered=False):
    col  = ACCENT if hovered else PANEL2
    tcol = DARK_BG if hovered else WHITE
    pygame.draw.rect(surf, col,  rect, border_radius=10)
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=10)
    lbl = font.render(text, True, tcol)
    surf.blit(lbl, lbl.get_rect(center=rect.center))


def username_screen():
    font_title = pygame.font.SysFont("Consolas", 38, bold=True)
    font_sub   = pygame.font.SysFont("Consolas", 18)
    font_input = pygame.font.SysFont("Consolas", 26, bold=True)

    name       = ""
    input_rect = pygame.Rect(100, 280, 400, 52)
    btn_start  = pygame.Rect(200, 370, 200, 46)

    while True:
        _gradient_bg(screen)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("SNAKE PRO", True, ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        sub = font_sub.render("Enter your username to begin", True, LIGHT_GRAY)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 195)))

        draw_panel(screen, input_rect.inflate(6, 6))
        lbl = font_input.render(name + "|", True, ACCENT)
        screen.blit(lbl, lbl.get_rect(center=input_rect.center))

        draw_button(screen, btn_start, "START", font_sub, btn_start.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif len(name) < 18:
                    name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.collidepoint(mx, my) and name.strip():
                    return name.strip()

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    font_title = pygame.font.SysFont("Consolas", 44, bold=True)
    font_sub   = pygame.font.SysFont("Consolas", 13)
    font_btn   = pygame.font.SysFont("Consolas", 20, bold=True)

    buttons = {
        "Play":        pygame.Rect(200, 230, 200, 48),
        "Leaderboard": pygame.Rect(175, 295, 250, 48),
        "Settings":    pygame.Rect(200, 360, 200, 48),
        "Quit":        pygame.Rect(200, 425, 200, 48),
    }

    while True:
        _gradient_bg(screen)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("SNAKE PRO", True, ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 130)))
        sub = font_sub.render("Eat. Grow. Survive.", True, LIGHT_GRAY)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 182)))

        for label, rect in buttons.items():
            draw_button(screen, rect, label, font_btn, rect.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return label

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    font_title = pygame.font.SysFont("Consolas", 30, bold=True)
    font_hdr   = pygame.font.SysFont("Consolas", 15, bold=True)
    font_row   = pygame.font.SysFont("Consolas", 15)
    font_btn   = pygame.font.SysFont("Consolas", 18, bold=True)
    btn_back   = pygame.Rect(200, 545, 200, 44)

    while True:
        _gradient_bg(screen)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("LEADERBOARD", True, ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 48)))

        board = get_leaderboard()
        hdr = font_hdr.render(f"{'#':<3} {'Username':<16} {'Score':>6}  {'Lvl':>4}  {'Date'}", True, ACCENT)
        screen.blit(hdr, (40, 88))
        pygame.draw.line(screen, ACCENT, (40, 108), (WIDTH - 40, 108), 1)

        for i, (uname, score, level, date) in enumerate(board):
            col = ACCENT if i == 0 else (LIGHT_GRAY if i < 3 else WHITE)
            row = font_row.render(
                f"{i+1:<3} {uname[:15]:<16} {score:>6}  {level:>4}  {date}",
                True, col
            )
            screen.blit(row, (40, 118 + i * 38))

        if not board:
            msg = font_row.render("No records yet. Be the first!", True, LIGHT_GRAY)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 300)))

        draw_button(screen, btn_back, "Back", font_btn, btn_back.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(mx, my):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)


def settings_screen(settings):
    font_title = pygame.font.SysFont("Consolas", 30, bold=True)
    font_lbl   = pygame.font.SysFont("Consolas", 18)
    font_btn   = pygame.font.SysFont("Consolas", 17, bold=True)

    btn_back  = pygame.Rect(175, 530, 250, 44)
    btn_grid  = pygame.Rect(350, 210, 110, 36)
    btn_sound = pygame.Rect(350, 270, 110, 36)

    COLORS = [
        ((60,  200, 80),  "Green"),
        ((0,   170, 220), "Cyan"),
        ((220, 80,  220), "Purple"),
        ((255, 200, 0),   "Yellow"),
        ((255, 100, 50),  "Orange"),
    ]
    color_btns = [
        (pygame.Rect(60 + i * 105, 370, 90, 36), rgb, name)
        for i, (rgb, name) in enumerate(COLORS)
    ]

    while True:
        _gradient_bg(screen)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("SETTINGS", True, ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        screen.blit(font_lbl.render("Grid overlay:", True, WHITE), (60, 217))
        grid_lbl = "ON" if settings["grid"] else "OFF"
        grid_col = GREEN if settings["grid"] else RED
        pygame.draw.rect(screen, grid_col, btn_grid, border_radius=8)
        screen.blit(font_btn.render(grid_lbl, True, WHITE), font_btn.render(grid_lbl, True, WHITE).get_rect(center=btn_grid.center))

        screen.blit(font_lbl.render("Sound:", True, WHITE), (60, 277))
        snd_lbl = "ON" if settings["sound"] else "OFF"
        snd_col = GREEN if settings["sound"] else RED
        pygame.draw.rect(screen, snd_col, btn_sound, border_radius=8)
        screen.blit(font_btn.render(snd_lbl, True, WHITE), font_btn.render(snd_lbl, True, WHITE).get_rect(center=btn_sound.center))

        screen.blit(font_lbl.render("Snake color:", True, WHITE), (60, 335))
        for rect, rgb, name in color_btns:
            active = list(settings["snake_color"]) == list(rgb)
            pygame.draw.rect(screen, rgb, rect, border_radius=8)
            if active:
                pygame.draw.rect(screen, ACCENT, rect, 3, border_radius=8)
            lbl = font_btn.render(name, True, WHITE)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        draw_button(screen, btn_back, "Save & Back", font_btn, btn_back.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_grid.collidepoint(mx, my):
                    settings["grid"] = not settings["grid"]
                    save_settings(settings)
                if btn_sound.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                    # Включить/выключить музыку сразу
                    if settings["sound"]:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                for rect, rgb, name in color_btns:
                    if rect.collidepoint(mx, my):
                        settings["snake_color"] = list(rgb)
                        save_settings(settings)
                if btn_back.collidepoint(mx, my):
                    save_settings(settings)
                    return

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score, level, personal_best):
    font_title = pygame.font.SysFont("Consolas", 40, bold=True)
    font_stat  = pygame.font.SysFont("Consolas", 20)
    font_btn   = pygame.font.SysFont("Consolas", 18, bold=True)

    btn_retry = pygame.Rect(80,  470, 180, 46)
    btn_menu  = pygame.Rect(340, 470, 180, 46)

    while True:
        _gradient_bg(screen)
        mx, my = pygame.mouse.get_pos()

        title = font_title.render("GAME OVER", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))

        panel = pygame.Rect(140, 220, 320, 210)
        draw_panel(screen, panel)

        new_best = score > personal_best
        stats = [
            ("Score",         str(score),  ACCENT),
            ("Level reached", str(level),  WHITE),
            ("Personal best", str(max(score, personal_best)),
             GREEN if new_best else LIGHT_GRAY),
        ]
        for i, (label, val, col) in enumerate(stats):
            screen.blit(font_stat.render(f"{label}:", True, LIGHT_GRAY), (160, 240 + i * 54))
            v = font_stat.render(val, True, col)
            screen.blit(v, (380, 240 + i * 54))

        if new_best:
            nb = font_stat.render("NEW BEST!", True, GREEN)
            screen.blit(nb, nb.get_rect(center=(WIDTH // 2, 415)))

        draw_button(screen, btn_retry, "Retry",     font_btn, btn_retry.collidepoint(mx, my))
        draw_button(screen, btn_menu,  "Main Menu", font_btn, btn_menu.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(mx, my):
                    return "retry"
                if btn_menu.collidepoint(mx, my):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def play_game(player_id, settings):
    game    = SnakeGame(player_id, settings)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.finish()
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                game.handle_key(event.key)

        alive = game.update()
        game.draw(screen)

        if not alive:
            game.finish()
            return game.score, game.level, game.personal_best

        pygame.display.flip()
        clock.tick(game.speed)


def main():
    init_db()
    settings = load_settings()
    username  = username_screen()
    player_id = get_or_create_player(username)

    while True:
        choice = main_menu()

        if choice == "Play":
            try:
                if settings.get("sound", True):
                    pygame.mixer.music.load("assets/frank-ocean-thinkin-bout-you.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"[Music error] {e}")

            while True:
                score, level, personal_best = play_game(player_id, settings)
                result = game_over_screen(score, level, personal_best)
                if result == "retry":
                    continue
                break

            # Останавливаем музыку когда вернулись в меню
            pygame.mixer.music.stop()

        elif choice == "Leaderboard":
            leaderboard_screen()

        elif choice == "Settings":
            settings_screen(settings)

        elif choice == "Quit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()