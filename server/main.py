from flask import Flask, request
from flask_cors import CORS
import numpy as np
from io import BytesIO
from PIL import Image
import keras
import cv2
from keras.applications.densenet import preprocess_input

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

MODEL = keras.models.load_model("D:\\Py for data science\\final project\\autism\\realtime\\model_1.h5")
CLASS_NAMES = ["Autistic", "Non_Autistic"]
video_capture = cv2.VideoCapture(1)  # Thử với index khác nhau

@app.route('/')
def read_root():
    return {"message": "Subscribe to @1littlecoder"}

@app.route('/ping')
def ping():
    return "Hello, I am alive"

@app.route('/predict_video', methods=['GET', 'POST'])
def predict_video():
    
    ret, frame = video_capture.read()

    if not ret:
        print("Error reading frame:", ret)
        return {"error": "Error reading frame"}


    resized_frame = cv2.resize(frame, (224, 224))
    image = preprocess_input(resized_frame)
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    print(predicted_class, " ", float(confidence))
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

@app.route('/predict_image', methods=['GET', 'POST'])
def predict_image():
    file = request.files['file']
    image = np.array(Image.open(BytesIO(file.read())))
    resized_frame = cv2.resize(image, (224, 224))
    image = preprocess_input(resized_frame)
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    print(predicted_class, " ", float(confidence))
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == '__main__':
    app.run(debug=True)
