import os
import json
import hashlib
import re

def generate_image_hash(image_path):
    """Generates a hash for an image file."""
    hasher = hashlib.md5()
    try:
        with open(image_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def sanitize_filename(name):
    """Removes invalid characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", name)