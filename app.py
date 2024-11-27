from flask import Flask, request, jsonify
from hashing_functions import calculate_file_hash, get_file_metadata, store_to_firebase
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Process file
        hash_value, metadata = calculate_file_hash(file_path), get_file_metadata(file_path)
        firebase_status = store_to_firebase(file.filename, hash_value, metadata)
        
        return jsonify({
            'filename': file.filename,
            'hash_value': hash_value,
            'metadata': metadata,
            'firebase_status': firebase_status
        })

if __name__ == '__main__':
    app.run(debug=True)
