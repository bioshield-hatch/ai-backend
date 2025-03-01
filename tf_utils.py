import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

keras = "plant.keras"
model = load_model(keras)
labels = ["Bacteria", "Fungus", "Healthy", "Pests", "Virus"]


def predict_image(filepath):
    detectimagething = filepath
    img = image.load_img(detectimagething, target_size=(256, 256))
    arayythingy = image.img_to_array(img)
    arayythingy = np.expand_dims(arayythingy, axis=0)
    arayythingy /= 255.0
    predictthingy = model.predict(arayythingy)
    predicted_class_index = np.argmax(predictthingy)
    label = labels[predicted_class_index]
    likelihood = predictthingy[0][predicted_class_index]
    return label, likelihood


