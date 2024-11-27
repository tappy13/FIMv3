# firebase_config.py
import firebase_admin
from firebase_admin import firestore

def upload_file_metadata_to_firestore(db, file_id, metadata):
    """
    Upload file metadata to Firestore.
    """
    doc_ref = db.collection("files").document(file_id)
    doc_ref.set(metadata)
    print(f"Metadata uploaded for file ID: {file_id}")

def check_file_in_firestore(db, file_id):
    """
    Check if a file exists in Firestore and retrieve its metadata.
    """
    doc_ref = db.collection("files").document(file_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"File found in Firestore with ID: {file_id}")
        return doc.to_dict()
    else:
        print(f"No file found with ID: {file_id}")
        return None

