from detect_emotion import detect_emotion
import pygame
import os
import random

# Initialize Pygame
pygame.mixer.init()

# Valid emotions (matching DeepFace output)
VALID_EMOTIONS = ['happy', 'sad', 'angry', 'neutral', 'surprise', 'fear', 'disgust']

# Detect emotion
emotion = detect_emotion()
print(f"Detected emotion: {emotion}")

# Validate emotion
if emotion not in VALID_EMOTIONS:
    print(f"Invalid emotion detected: {emotion}. Defaulting to 'neutral'.")
    emotion = 'neutral'

# Load and play music
music_folder = f"music/{emotion}"
try:
    songs = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    if songs:
        selected_song = os.path.join(music_folder, random.choice(songs))
        print(f"Playing song: {selected_song}")
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Prevent high CPU usage
    else:
        print(f"No songs found for emotion '{emotion}' in {music_folder}.")
except FileNotFoundError:
    print(f"Music folder for emotion '{emotion}' not found: {music_folder}")
except Exception as e:
    print(f"Error playing music: {e}")
finally:
    pygame.mixer.quit()