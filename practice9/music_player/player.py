import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        # Load all wav/mp3 files from the directory
        self.playlist = [f for f in os.listdir(music_dir) if f.endswith(('.wav', '.mp3'))]
        self.current_index = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return
        
        # If we were stopped, load and play; if paused, unpause
        if not self.is_playing:
            path = os.path.join(self.music_dir, self.playlist[self.current_index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.is_playing = True
        else:
            pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.is_playing = False
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No Music Found"
        return self.playlist[self.current_index]