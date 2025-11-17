import os
import json
import shutil

def organize_attachments(processed_json_path, pptx_file_name):
    """
    Organizes attachments into a subfolder named after the Markdown note.
    """
    with open(processed_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_name = os.path.splitext(pptx_file_name)[0]
    
    attachments_root_dir = os.path.join(os.path.dirname(processed_json_path), "attachments")
    
    note_attachments_dir = os.path.join(attachments_root_dir, base_name)
    if not os.path.exists(note_attachments_dir):
        os.makedirs(note_attachments_dir)

    for slide in data["slides"]:
        updated_image_paths = []
        for img_path in slide["images"]:
            if os.path.exists(img_path):
                filename = os.path.basename(img_path)
                destination_path = os.path.join(note_attachments_dir, filename)
                shutil.move(img_path, destination_path)
                
                relative_path = os.path.join("attachments", base_name, filename).replace(os.sep, '/')
                updated_image_paths.append(relative_path)
            else:
                # This handles duplicates that were already moved
                filename = os.path.basename(img_path)
                relative_path = os.path.join("attachments", base_name, filename).replace(os.sep, '/')
                updated_image_paths.append(relative_path)


        slide["images"] = updated_image_paths

    final_json_path = os.path.join(os.path.dirname(processed_json_path), "final_content.json")
    with open(final_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return final_json_path
