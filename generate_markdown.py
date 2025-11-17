import os
import json

def generate_markdown(final_json_path, pptx_file_name):
    """
    Generates the Markdown file from the processed content.
    """
    with open(final_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_name = os.path.splitext(pptx_file_name)[0]
    output_dir = os.path.dirname(final_json_path)
    md_file_path = os.path.join(output_dir, f"{base_name}.md")

    markdown_lines = []

    for slide in data["slides"]:
        if slide["text"]:
            markdown_lines.append("\n".join(slide["text"]))
        
        for img_path_relative in slide["images"]:
            markdown_lines.append(f"![image]({img_path_relative})")
        
        markdown_lines.append("\n---\n")

    if markdown_lines and markdown_lines[-1] == "\n---\n":
        markdown_lines.pop()

    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_lines))

    return md_file_path
