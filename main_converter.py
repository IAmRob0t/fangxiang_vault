import os
import shutil
from extract_content import extract_pptx_content
from process_images import process_images
from organize_attachments import organize_attachments
from generate_markdown import generate_markdown
from optimize_markdown import optimize_markdown

def main_conversion_workflow(pptx_file_path):
    """
    Orchestrates the entire PPTX to Markdown conversion process.
    """
    if not os.path.exists(pptx_file_path):
        print(f"Error: Source file not found at {pptx_file_path}")
        return

    base_output_dir = os.path.dirname(pptx_file_path)
    pptx_file_name = os.path.basename(pptx_file_path)
    
    # --- Workflow ---
    print("Step 1: Extracting content...")
    extracted_json_path = extract_pptx_content(pptx_file_path, base_output_dir)

    print("\nStep 2: Processing images...")
    processed_json_path = process_images(extracted_json_path)

    print("\nStep 3: Organizing attachments...")
    final_json_path = organize_attachments(processed_json_path, pptx_file_name)

    print("\nStep 4: Generating Markdown...")
    generated_md_path = generate_markdown(final_json_path, pptx_file_name)

    print("\nStep 5: Optimizing Markdown...")
    optimized_md_path = optimize_markdown(generated_md_path, pptx_file_name)

    print(f"\nConversion complete. Final Markdown file: {optimized_md_path}")

    # --- Cleanup ---
    print("\nStep 6: Cleaning up temporary files...")
    temp_files = [
        extracted_json_path,
        processed_json_path,
        final_json_path,
        pptx_file_path
    ]
    
    # Also remove the script files themselves as per the prompt's philosophy
    script_files = [
        "extract_content.py", "process_images.py", "organize_attachments.py",
        "generate_markdown.py", "optimize_markdown.py", "main_converter.py"
    ]
    temp_files.extend(script_files)


    for f_path in temp_files:
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"  - Deleted: {f_path}")
            except Exception as e:
                print(f"  - Error deleting {f_path}: {e}")
    
    # Clean up __pycache__ if it exists
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("  - Deleted: __pycache__ directory")

    print("Cleanup finished.")


if __name__ == "__main__":
    pptx_source_path = "00_Inbox/02_ARM内部寄存器.pptx"
    main_conversion_workflow(pptx_source_path)
