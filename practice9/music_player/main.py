import pygame
import sys
from player import MusicPlayer

# Constants
WIDTH, HEIGHT = 500, 300
FPS = 30
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 255, 127)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Keyboard Music Player")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)

    
    import os

    # Get the directory where main.py is located
    base_path = os.path.dirname(__file__)
    music_folder = os.path.join(base_path, "music")

    # Now initialize the player with the smart path
    player = MusicPlayer(music_folder)

    running = True
    while running:
        screen.fill(BLACK)

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # Play
                    player.play()
                elif event.key == pygame.K_s: # Stop
                    player.stop()
                elif event.key == pygame.K_n: # Next
                    player.next_track()
                elif event.key == pygame.K_b: # Back/Previous
                    player.prev_track()
                elif event.key == pygame.K_q: # Quit
                    running = False

        # 2. Logic (Progress calculation)
        # mixer.music.get_pos() returns ms since song started
        pos_ms = pygame.mixer.music.get_pos()
        progress_text = f"Position: {max(0, pos_ms // 1000)}s" if player.is_playing else "Status: Stopped"

        # 3. Rendering UI
        # Display Track Name
        track_surface = font.render(f"Now Playing: {player.get_current_track_name()}", True, WHITE)
        screen.blit(track_surface, (50, 80))

        # Display Progress
        progress_surface = small_font.render(progress_text, True, GREEN)
        screen.blit(progress_surface, (50, 120))

        # Display Controls Legend
        controls_text = "P: Play | S: Stop | N: Next | B: Back | Q: Quit"
        controls_surface = small_font.render(controls_text, True, (150, 150, 150))
        screen.blit(controls_surface, (50, 220))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()