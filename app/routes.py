import os
from flask import Flask, jsonify, url_for, send_from_directory, redirect, render_template, request
from app import app
from werkzeug.utils import secure_filename
import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import img_to_array

# import form from app.forms and set route for upload

def get_model():
    global model
    model = load_model('mn_dnd_model.h5')
    print(' * Model loaded!')

def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image.astype('float32')
    image = (image - 127.5) / 127.5
    image = np.expand_dims(image, axis=0)

    return image

print(' * Loading Keras model...')
get_model()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),"images")
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


#---------------- IMAGE UPLOAD--------------------

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return "failure at 1"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return "failure at 2"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #filename to random string maybe. gotta keep extensions!
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return url_for('uploaded_file', filename=filename)

    
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#----------------------------------------------------

@app.route('/predictdnd', methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()
    
    response = {
        'prediction': {
            'barbarian': prediction[0][0],
            'bard': prediction[0][1],
            'cleric': prediction[0][2],
            'druid': prediction[0][3],
            'fighter': prediction[0][4],
            'mage': prediction[0][5],
            'monk': prediction[0][6],
            'paladin': prediction[0][7],
            'rogue': prediction[0][8],
            'sorcerer': prediction[0][9],
            'warlock': prediction[0][10],
            'wizard': prediction[0][11]
        }
    }
    return jsonify(response)

@app.route('/result')
def result():
    return render_template('result.html')