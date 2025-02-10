import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Load the pre-trained MobileNetV2 model for plant identification
model = MobileNetV2(weights="imagenet")

def process_image(image_path):
    """Process the image to identify the plant and determine its health grade."""
    
    # Load and preprocess image for model prediction
    img = image.load_img(image_path, target_size=(224, 224))  # Resize image to match model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Normalize image

    # Predict plant species
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    plant_name = decoded_predictions[0][1]  # Extract the most probable plant name

    # Convert image to OpenCV format
    cv_img = cv2.imread(image_path)
    hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)

    # Detect green color (chlorophyll content analysis)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = np.sum(mask == 255)
    total_pixels = mask.size
    green_percentage = (green_pixels / total_pixels) * 100

    # Texture analysis using grayscale contrast
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray)

    # Assign a grade based on chlorophyll and texture analysis
    if green_percentage > 70 and std_dev < 10:
        grade = "Excellent"
    elif green_percentage > 50 and std_dev < 15:
        grade = "Good"
    elif green_percentage > 30:
        grade = "Fair"
    else:
        grade = "Poor"

    return plant_name, grade, std_dev, green_percentage
