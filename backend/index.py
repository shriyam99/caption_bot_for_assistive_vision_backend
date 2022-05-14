import flask
import io
import string
import time
import sys
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS


model = tf.keras.models.load_model('my_model')

def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    return img

def predict_result(img):
    return model.predict(img)

app = Flask(__name__)

cors = CORS(app)
@app.route('/predict', methods=['POST'])
def infer_image():
    if 'file' not in request.files:
        return jsonify(r = "Please try again. The Image doesn't exist")
    
    file = request.files.get('file')
    
    if not file:
        return

    img_bytes = file.read()
    img = prepare_image(img_bytes)
    
    return jsonify(prediction=predict_result(img))
    

@app.route('/', methods=['GET'])
def index():
    return 'Machine Learning Inference'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')