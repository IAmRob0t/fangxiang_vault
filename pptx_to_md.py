import os
import shutil
from extract_pptx_content import extract_pptx_content
from process_images import process_images

def pptx_to_md_converter(pptx_file_path):
    # Define paths
    base_name = os.path.splitext(os.path.basename(pptx_file_path))[0]
    output_dir = os.path.dirname(pptx_file_path)
    attachments_dir = os.path.join(output_dir, "attachments")
    md_file_name = f"{base_name}.md"
    md_file_path = os.path.join(output_dir, md_file_name)
    extracted_text_file = os.path.join(output_dir, "extracted_text.txt")

    # Step 1: Extract content
    print(f"Extracting content from {pptx_file_path}...")
    all_text_slides, slide_image_map = extract_pptx_content(pptx_file_path, attachments_dir)
    print("Content extraction complete.")

    # Step 2: Process images (deduplicate, rename)
    print("Processing images...")
    image_mapping = process_images(attachments_dir)
    print("Image processing complete.")

    # Step 3: Organize attachments (create subfolder and move images)
    print("Organizing attachments...")
    note_attachments_dir = os.path.join(attachments_dir, base_name)
    if not os.path.exists(note_attachments_dir):
        os.makedirs(note_attachments_dir)

    final_image_map = {}
    for original_full_path, processed_full_path in image_mapping.items():
        # Get just the filename from the processed_full_path
        processed_filename = os.path.basename(processed_full_path)
        destination_path = os.path.join(note_attachments_dir, processed_filename)
        shutil.move(processed_full_path, destination_path)
        # Store the relative path for Markdown
        final_image_map[original_full_path] = os.path.join("attachments", base_name, processed_filename)
    print(f"Attachments organized into {note_attachments_dir}")

    # Step 4: Generate Markdown
    print("Generating Markdown note...")
    markdown_content_blocks = []
    for i, slide_text_block in enumerate(all_text_slides):
        markdown_content_blocks.append(slide_text_block)
        slide_num = i + 1
        if slide_num in slide_image_map:
            for original_image_path in slide_image_map[slide_num]:
                if original_image_path in final_image_map:
                    relative_image_path = final_image_map[original_image_path]
                    markdown_content_blocks.append(f"\n![]({relative_image_path})\n")

    # Step 5: Optimize Markdown (Frontmatter, Heading Levels)
    print("Optimizing Markdown note...")
    final_markdown_lines = []

    # Add Frontmatter
    # For now, hardcode tags based on the example. In a real scenario, this would be inferred.
    tags = ["ARM", "汇编", "指令集"]
    frontmatter = [
        "---",
        "tags:",
        *[f"  - {tag}" for tag in tags],
        "---"
    ]
    final_markdown_lines.extend(frontmatter)
    final_markdown_lines.append("") # Add a blank line after frontmatter

    # Adjust Heading Levels
    first_h1_found = False
    for block in markdown_content_blocks:
        for line in block.split('\n'):
            if line.startswith('#'):
                if not first_h1_found:
                    # Remove the very first H1
                    if line.startswith('# '):
                        first_h1_found = True
                        continue
                # Promote other headings
                if line.startswith('## '):
                    final_markdown_lines.append(f"# {line[3:]}")
                elif line.startswith('### '):
                    final_markdown_lines.append(f"## {line[4:]}")
                elif line.startswith('#### '):
                    final_markdown_lines.append(f"### {line[5:]}")
                elif line.startswith('##### '):
                    final_markdown_lines.append(f"#### {line[6:]}")
                elif line.startswith('###### '):
                    final_markdown_lines.append(f"##### {line[7:]}")
                else: # Keep other H1s as H1 if not the very first one
                    final_markdown_lines.append(line)
            else:
                final_markdown_lines.append(line)

    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_markdown_lines))
    print(f"Markdown note generated and optimized at {md_file_path}")

    # Step 6: Cleanup
    print("Cleaning up temporary files...")
    if os.path.exists(extracted_text_file):
        os.remove(extracted_text_file)
    if os.path.exists("extract_pptx_content.py"):
        os.remove("extract_pptx_content.py")
    if os.path.exists("process_images.py"):
        os.remove("process_images.py")
    if os.path.exists(pptx_file_path):
        os.remove(pptx_file_path)
    print("Cleanup complete.")

    print("Conversion process finished.")

if __name__ == "__main__":
    pptx_file = "00_Inbox/04_ARM汇编模拟器VisUAL.pptx"
    pptx_to_md_converter(pptx_file)
