import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
keras = "plant.keras"  
model = load_model(keras)
labels = ["Bacteria", "Fungus", "Healthy", "Pests", "Virus"]
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def predict_image(filepath):
    detectimagething = filepath
    img = image.load_img(detectimagething, target_size=(256, 256))
    arayythingy = image.img_to_array(img)
    arayythingy = np.expand_dims(arayythingy, axis=0)
    arayythingy /= 255.0
    predictthingy = model.predict(arayythingy)
    predicted_class_index = np.argmax(predictthingy)
    guh = labels[predicted_class_index]
    guh2 = predictthingy[0][predicted_class_index]
    return guh, guh2

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        guh, guh2 = predict_image(filepath)
        return render_template("index.html", filename=filename, label=guh, confidence=guh2 * 100)
    return render_template("index.html", filename=None, label=None, confidence=None)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return redirect(url_for("static", filename=f"uploads/{filename}"))

if __name__ == "__main__":
    app.run(debug=True)
