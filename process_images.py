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
        print(f"Error: Image file not found at {image_path}")
        return None

def sanitize_filename(name):
    """Removes invalid characters from a filename."""
    # Remove newlines and other problematic whitespace first
    name = name.replace('
', ' ').replace('', '')
    # Then remove other invalid characters
    return re.sub(r'[^\w\s\u4e00-\u9fa5.-]', '', name).strip()

def generate_image_name_from_text(text_list, slide_number, image_index):
    """
    Simulates intelligent naming by finding keywords in slide text.
    """
    # Sort by length, shortest first, as titles are often short
    sorted_text = sorted(text_list, key=len)

    for text in sorted_text:
        if 2 < len(text.strip()) < 50: # Assume a reasonable title length
            clean_name = sanitize_filename(text.strip())
            if clean_name:
                return f"{clean_name}"

    return f"幻灯片{slide_number}的图片{image_index + 1}"

def process_images(json_path):
    """
    Deduplicates and renames images based on slide context.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    unique_images = {}  # hash -> new_path
    
    for slide in data["slides"]:
        updated_image_paths = []
        for i, img_path in enumerate(slide["images"]):
            img_hash = generate_image_hash(img_path)
            if not img_hash:
                continue

            if img_hash in unique_images:
                updated_image_paths.append(unique_images[img_hash])
                if os.path.exists(img_path):
                    os.remove(img_path)
            else:
                ext = os.path.splitext(img_path)[1]
                base_name_suggestion = generate_image_name_from_text(slide["text"], slide["slide_number"], i)
                
                new_filename_base = base_name_suggestion
                new_filename = f"{new_filename_base}{ext}"
                
                current_dir = os.path.dirname(img_path)
                new_filepath = os.path.join(current_dir, new_filename)

                counter = 1
                while os.path.exists(new_filepath) and new_filepath != img_path:
                    new_filename = f"{new_filename_base}_{counter}{ext}"
                    new_filepath = os.path.join(current_dir, new_filename)
                    counter += 1

                if os.path.exists(img_path):
                    os.rename(img_path, new_filepath)
                    unique_images[img_hash] = new_filepath
                    updated_image_paths.append(new_filepath)

        slide["images"] = updated_image_paths

    processed_json_path = os.path.join(os.path.dirname(json_path), "processed_content.json")
    with open(processed_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return processed_json_path
