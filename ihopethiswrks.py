import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

label = ["Bacteria", "Fungus", "Healthy", "Pests", "Virus"]
keras = "plant.keras"  
model = load_model(keras)
detectimagething = "vir (10017).jpg"  
img = image.load_img(detectimagething, target_size=(256, 256))  
arayythingy = image.img_to_array(img)
arayythingy = np.expand_dims(arayythingy, axis=0)  
arayythingy /= 255.0  
predictthingy = model.predict(arayythingy)
predicted_class_index = np.argmax(predictthingy) 
guh = label[predicted_class_index] 
guh2 = predictthingy[0][predicted_class_index]  
plt.imshow(img)
plt.axis("off")
plt.title("Input Image")
plt.show()
print("Raw model output:", predictthingy)
print(f"Predicted label: {guh} ({guh2 * 100:.2f}% confidence)")