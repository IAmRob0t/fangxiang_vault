import os
import re

def optimize_markdown(md_file_path, pptx_file_name):
    """
    Optimizes the Markdown file by adding frontmatter, adjusting heading levels,
    and performing basic text refinement.
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content_lines = f.readlines()

    optimized_lines = []

    # Infer tags from filename/content (simple example)
    tags = ["ARM", "汇编"]
    if "寄存器" in pptx_file_name:
        tags.append("内部寄存器")

    frontmatter = [
        "---",
        "tags:",
        *[f"  - {tag}" for tag in tags],
        "---",
        ""
    ]
    optimized_lines.extend(frontmatter)

    first_h1_found = False
    for line in content_lines:
        stripped_line = line.strip()

        if not stripped_line and (not optimized_lines or not optimized_lines[-1].strip()):
            continue

        if stripped_line.startswith('#'):
            if not first_h1_found and stripped_line.startswith('# '):
                first_h1_found = True
                continue
            else:
                if stripped_line.startswith('## '):
                    optimized_lines.append(f"# {stripped_line[3:]}")
                elif stripped_line.startswith('### '):
                    optimized_lines.append(f"## {stripped_line[4:]}")
                else:
                    optimized_lines.append(stripped_line)
        else:
            optimized_lines.append(stripped_line)
    
    if optimized_lines and optimized_lines[-1] != "":
        optimized_lines.append("")

    with open(md_file_path, 'w', encoding="utf-8") as f:
        f.write("\n".join(optimized_lines))

    return md_file_path
