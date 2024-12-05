#!/usr/bin/env python3
gfgfgfhfghfg
from flask import Flask, request, render_template, jsonify
import cv2
import pytesseract
from music21 import *
import numpy as np
from PIL import Image
import pygame
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_sheet_music(image_path):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply image preprocessing
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Use pytesseract for initial OCR (this is a basic implementation)
    # In a production environment, you'd want to use a specialized OMR library
    text = pytesseract.image_to_string(thresh)
    
    # Convert to music21 stream (simplified example)
    # In reality, you'd need more sophisticated parsing
    score = converter.parse(text)
    return score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            score = process_sheet_music(filepath)
            # Convert to MIDI for playback
            midi_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mid')
            score.write('midi', midi_path)
            
            return jsonify({
                'success': True,
                'message': 'File processed successfully',
                'midi_file': 'output.mid'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/play/<filename>')
def play_midi(filename):
    midi_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(midi_path):
        return jsonify({'error': 'MIDI file not found'}), 404
    
    pygame.mixer.init()
    pygame.mixer.music.load(midi_path)
    pygame.mixer.music.play()
    
    return jsonify({'success': True, 'message': 'Playing music'})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)
