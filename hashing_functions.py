import hashlib
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate('./firebase_config.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_file_metadata(file_path):
    """Extract basic file metadata."""
    try:
        metadata = {
            'file_size': os.path.getsize(file_path),
            'file_name': os.path.basename(file_path),
        }
        return metadata
    except Exception as e:
        return {'error': str(e)}

def store_to_firebase(filename, hash_value, metadata):
    """Store file data to Firebase."""
    try:
        db.collection('files').document(filename).set({
            'hash_value': hash_value,
            'metadata': metadata
        })
        return "Successfully stored in Firebase."
    except Exception as e:
        return f"Error storing in Firebase: {e}"
