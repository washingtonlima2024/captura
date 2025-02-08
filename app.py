# Backend: app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

photo_counter = 1

# Route to handle photo uploads
@app.route('/api/upload', methods=['POST'])
def upload_photo():
    global photo_counter
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f'exame_{photo_counter}.png'
    photo_counter += 1
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({'filePath': f'/uploads/{filename}'}), 200

# Route to serve uploaded files
@app.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to serve icon files
@app.route('/icone/<filename>', methods=['GET'])
def get_icon_file(filename):
    return send_from_directory('frontend/icone', filename)

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)