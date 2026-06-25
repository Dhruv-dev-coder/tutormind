import os
import json
from typing import Optional, Dict, Any

import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    cred_data = os.getenv('FIREBASE_CREDENTIALS')
    if not cred_data:
        # No credentials provided; skip initialization (useful for local testing)
        return None

    try:
        # If FIREBASE_CREDENTIALS is a path to a file
        if os.path.exists(cred_data):
            cred = credentials.Certificate(cred_data)
        else:
            # Assume it's a JSON string
            cred_json = json.loads(cred_data)
            cred = credentials.Certificate(cred_json)
        app = firebase_admin.initialize_app(cred)
        return app
    except Exception:
        # Initialization failed; re-raise or return None to allow graceful degradation
        raise


def verify_id_token(id_token: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase ID token and return decoded token payload.

    Returns None if verification fails or Firebase is not initialized.
    """
    if not firebase_admin._apps:
        try:
            initialize_firebase()
        except Exception as e:
            # Log the error for debugging
            print(f"Firebase initialization failed: {e}")
            return None
    
    if not firebase_admin._apps:
        print("Firebase not initialized - check FIREBASE_CREDENTIALS environment variable")
        return None
    
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
