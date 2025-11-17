import os
import json
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def extract_pptx_content(pptx_path, base_output_dir):
    """
    Extracts text and images from a PPTX file and saves them.
    """
    attachments_dir = os.path.join(base_output_dir, "attachments")
    if not os.path.exists(attachments_dir):
        os.makedirs(attachments_dir)

    prs = Presentation(pptx_path)
    
    extracted_data = {
        "slides": []
    }

    for i, slide in enumerate(prs.slides):
        slide_number = i + 1
        slide_content = {
            "slide_number": slide_number,
            "text": [],
            "images": []
        }

        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text = shape.text.strip()
                if text:
                    slide_content["text"].append(text)

        image_index = 0
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                image = shape.image
                image_bytes = image.blob
                image_ext = image.ext.lower()
                
                image_filename = f"slide_{slide_number}_image_{image_index + 1}.{image_ext}"
                image_path = os.path.join(attachments_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                slide_content["images"].append(image_path)
                image_index += 1
        
        extracted_data["slides"].append(slide_content)

    json_output_path = os.path.join(base_output_dir, "extracted_content.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Content extracted to {json_output_path}")
    return json_output_path
