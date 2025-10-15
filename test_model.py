import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np

# Load the trained model
model = load_model('emotion_model.h5')

# Define emotion labels (matching FER2013 dataset)
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Load and preprocess a sample image (e.g., from fer2013/test/happy)
# Replace 'fer2013/test/happy/0.jpg' with any image path from your dataset
image_path = 'fer2013/test/sad/0.jpg'  # Example path; adjust as needed
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Could not load image. Check the file path.")
else:
    # Resize to 48x48 (model input size)
    img = cv2.resize(img, (48, 48))
    # Normalize pixel values
    img = img / 255.0
    # Reshape for model prediction (add batch dimension)
    img = img.reshape(1, 48, 48, 1)

    # Make prediction
    prediction = model.predict(img)
    emotion = emotions[np.argmax(prediction)]
    confidence = np.max(prediction) * 100  # Convert to percentage

    # Display result
    print(f"Predicted emotion: {emotion} (Confidence: {confidence:.2f}%)")
    print(f"Prediction probabilities: {prediction[0]}")