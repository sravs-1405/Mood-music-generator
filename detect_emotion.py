import cv2
import tensorflow as tf
import pandas as pd
from tensorflow.keras.models import load_model
import time

print("Starting detect_emotion.py...")

# Load the model
try:
    model = load_model('emotion_model.keras')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load music dataset (fallback if missing)
try:
    music_df = pd.read_csv('music_emotion_mapping.csv')
    music_mapping = {row['emotion']: (row['track_name'], row['artist'], row['preview_url']) for _, row in music_df.iterrows()}
    print("Music dataset loaded successfully. Mapping:", music_mapping)
except FileNotFoundError:
    print("Warning: music_emotion_mapping.csv not found. Using default fallback.")
    music_mapping = {"neutral": ("No track", "N/A", None)}
except Exception as e:
    print(f"Error loading music dataset: {e}. Using default fallback.")
    music_mapping = {"neutral": ("No track", "N/A", None)}

def detect_emotion():
    print("Entering detect_emotion function...")
    if model is None:
        print("Error: Model not loaded. Yielding fallback.")
        yield (None, "neutral", "Error: Model failed to load.", ("No track", "N/A", None))
        return

    print("Attempting webcam initialization...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(1)  # Give time for webcam to initialize
    if not cap.isOpened():
        print("Warning: Webcam not found. Yielding fallback.")
        yield (None, "neutral", "Warning: No webcam found.", ("No track", "N/A", None))
    else:
        print("Webcam opened successfully.")
        for _ in range(2):  # Yield twice to ensure processing
            yield (None, "neutral", "Webcam initialized.", music_mapping.get("neutral", ("No track", "N/A", None)))
        cap.release()

    print("Exiting detect_emotion function.")

if __name__ == "__main__":
    for item in detect_emotion():
        print(f"Yielded: {item}")