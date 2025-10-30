# import tensorflow as tf
# import numpy as np
# from tensorflow.keras.preprocessing import image

# def predict_flower(model_path, img_path):
#     model = tf.keras.models.load_model(model_path)
#     img = image.load_img(img_path, target_size=(180, 180))
#     img_array = image.img_to_array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     prediction = model.predict(img_array)
#     class_names = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']
#     result = class_names[np.argmax(prediction)]
#     confidence = np.max(prediction)
#     return result, confidence

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import os

def predict_flower(model_path, img_path):
    # Load the model once
    model = tf.keras.models.load_model(model_path)

    # Ensure consistent image format
    img = Image.open(img_path).convert("RGB")
    img = img.resize((180, 180))

    # Convert to numpy array and normalize
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    confidence = float(np.max(prediction))
    predicted_index = int(np.argmax(prediction))

    # Dynamically fetch class names (safe option)
    class_dir = "data/flowers"
    class_names = sorted(os.listdir(class_dir))  # ensures same order as training
    print("Class names used for prediction:", class_names)

    # Handle mismatch case
    label = class_names[predicted_index] if predicted_index < len(class_names) else "Unknown"

    return label, confidence
