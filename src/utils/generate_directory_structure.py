import os
from utils.logger import log


# Helper Function to create project structure in the readme. Copy the printed project structure directly into the readme.
def generate_directory_structure(start_path, indent="    "):
    output = []
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)
        indent_level = indent * level
        output.append(f"{indent_level}├── {os.path.basename(root)}/")
        sub_indent = indent * (level + 1)
        for f in files:
            output.append(f"{sub_indent}├── {f}")
    return "\n".join(output)


if __name__ == "__main__":
    # Specify the starting path for your project
    start_path = "src"

    # Generate the directory structure
    directory_structure = generate_directory_structure(start_path)

    # Print the result
    log.info(directory_structure)
