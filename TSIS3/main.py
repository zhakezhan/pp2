import pygame
import sys
from ui import main_menu, settings_screen, leaderboard_screen, game_over_screen, username_screen
from racer import run_game
from persistence import load_settings, save_score

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

surf  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Racer Pro")


def main():
    settings = load_settings()
    username = None

    while True:
        choice = main_menu(surf, clock)

        if choice == "Play":
            if username is None:
                username = username_screen(surf, clock)

            while True:
                score, distance, coins = run_game(surf, clock, username, settings)
                save_score(username, score, distance, coins)
                result = game_over_screen(surf, clock, score, distance, coins)

                if result == "retry":
                    continue
                else:
                    break

        elif choice == "Leaderboard":
            leaderboard_screen(surf, clock)

        elif choice == "Settings":
            settings_screen(surf, clock, settings)

        elif choice == "Quit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()