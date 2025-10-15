import streamlit as st
from detect_emotion import detect_emotion
import cv2
import numpy as np
from PIL import Image

st.title("Mood Music Generator")
st.write("Detect your emotion and get music recommendations!")

# Mode selection
mode = st.radio("Select Mode:", ["Automatic Detection", "Manual Selection"])

if mode == "Automatic Detection":
    st.write("Using webcam for real-time emotion detection...")
    placeholder = st.empty()
    emotion = None
    music_info = None

    for item in detect_emotion():
        st.write(f"Received item: {item}")  # Log the raw item
        if item is None:
            st.write("Skipping None item")
            continue
        try:
            frame, detected_emotion, message, (track_name, artist, preview_url) = item
            if message:
                st.write(message)
            if detected_emotion:
                emotion = detected_emotion
                music_info = (track_name, artist, preview_url)
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                placeholder.image(frame, channels="RGB", use_column_width=True)
        except ValueError as e:
            st.write(f"Error unpacking item: {e}")
            continue

    if emotion and music_info:
        st.success(f"Detected Emotion: {emotion}")
        st.write(f"Recommended Track: {music_info[0]} by {music_info[1]}")
        if music_info[2]:
            st.audio(music_info[2], format="audio/mp3")
        else:
            st.warning("No preview available for this track.")
    else:
        st.warning("No valid emotion detected. Check setup.")

elif mode == "Manual Selection":
    st.write("Select your mood manually:")
    emotion_options = ["neutral"]  # Simplified for testing
    selected_emotion = st.selectbox("Choose an emotion:", emotion_options)
    track_name, artist, preview_url = "No track", "N/A", None

    if st.button("Get Music"):
        st.success(f"Selected Emotion: {selected_emotion}")
        st.write(f"Recommended Track: {track_name} by {artist}")
        st.warning("No preview available for this track.")