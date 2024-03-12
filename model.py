import os
import numpy as np
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array
from skimage.transform import resize
import tensorflow as tf
from keras.applications.vgg16 import preprocess_input
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest


# Your disease labels
disease_labels = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___health"
]

# Load your .h5 model
custom_objects = {'GlorotUniform': tf.keras.initializers.GlorotUniform()}
model = tf.keras.models.load_model('best_model.h5', compile=False, custom_objects=custom_objects)


def predict_disease(image_path):
    if os.path.exists(image_path):
        predicted_class = process_and_predict(image_path)
        if predicted_class:
            return (f'Predicted Disease: {predicted_class}')
        else:
            return ('Error in prediction')
    else:
        return ('Invalid image path')


def process_and_predict(image_path):
    img = load_img(image_path, target_size=(256, 256))

    i = img_to_array(img)
    im = preprocess_input(i)
    img = np.expand_dims(im, axis=0)
    preds = model.predict(img)

    if preds.shape[1] == len(disease_labels):
        pred_index = np.argmax(preds)
        predicted_class = disease_labels[pred_index]
        return predicted_class
    else:
        return None