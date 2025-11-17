import os
import shutil
import json

# Assuming these scripts are in the same directory
from extract_content import extract_pptx_content
from process_images import process_images
from organize_attachments import organize_attachments
from generate_markdown import generate_markdown
from optimize_markdown import optimize_markdown

def main_conversion_workflow(pptx_file_path):
    base_output_dir = os.path.dirname(pptx_file_path)
    pptx_file_name = os.path.basename(pptx_file_path)
    md_file_name = os.path.splitext(pptx_file_name)[0] + ".md"
    md_file_full_path = os.path.join(base_output_dir, md_file_name)

    # Step 1: Extract content
    extracted_json_path = extract_pptx_content(pptx_file_path, base_output_dir)

    # Step 2: Process images
    processed_json_path = process_images(extracted_json_path)

    # Step 3: Organize attachments
    final_json_path = organize_attachments(processed_json_path, pptx_file_name)

    # Step 4: Generate Markdown
    generated_md_path = generate_markdown(final_json_path, pptx_file_name)

    # Step 5: Optimize Markdown
    optimized_md_path = optimize_markdown(generated_md_path, pptx_file_name)

    print(f"\nConversion complete. Final Markdown file: {optimized_md_path}")

    # Cleanup (as per original request)
    print("\nStarting cleanup...")
    temp_files = [
        "extract_content.py",
        "process_images.py",
        "organize_attachments.py",
        "generate_markdown.py",
        "optimize_markdown.py",
        extracted_json_path,
        processed_json_path,
        final_json_path,
        pptx_file_path # Delete original PPTX
    ]

    for f_path in temp_files:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"Deleted: {f_path}")
            except Exception as e:
                print(f"Error deleting {f_path}: {e}")
    
    # Check if the attachments root directory is empty after moving files
    attachments_root_dir = os.path.join(base_output_dir, "attachments")
    if os.path.exists(attachments_root_dir) and not os.listdir(attachments_root_dir):
        try:
            os.rmdir(attachments_root_dir)
            print(f"Deleted empty attachments root directory: {attachments_root_dir}")
        except Exception as e:
            print(f"Error deleting empty attachments root directory {attachments_root_dir}: {e}")

    print("Cleanup finished.")


if __name__ == "__main__":
    # Ensure the PPTX file is present for the workflow to run
    # For this demonstration, we assume the user has placed it back.
    pptx_source_path = "00_Inbox/04_ARM汇编模拟器VisUAL.pptx"
    
    # Create dummy scripts for import if they don't exist yet (for initial run)
    # In a real scenario, these would be created by the agent or user.
    script_names = ["extract_content.py", "process_images.py", "organize_attachments.py", "generate_markdown.py", "optimize_markdown.py"]
    for script_name in script_names:
        if not os.path.exists(script_name):
            with open(script_name, 'w') as f:
                f.write("# Dummy script for import\npass\n")

    main_conversion_workflow(pptx_source_path)
