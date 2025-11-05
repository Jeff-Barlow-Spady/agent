import os
import os.path
import sys

from google.genai import types

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def write_file(working_directory, file_path, content):
    """
    Write content to a file within a specified working directory.

    This function is designed to be safe for LLM agents by:
    1. Preventing access outside the working directory (security)
    2. Always returning strings (LLM-friendly)
    3. Handling all errors gracefully
    """

    # STEP 1: PATH CONSTRUCTION AND VALIDATION
    # ==========================================

    # Convert working directory to absolute path first (cleaner approach)
    abs_working_dir = os.path.abspath(working_directory)

    # Join paths and convert to absolute path immediately
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    # SECURITY CHECK: Ensure the requested path stays within working directory boundaries
    # This prevents the LLM from accessing files outside its permitted area
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # STEP 2: FILE VALIDATION
    # =========================

    # Check if the path actually exists and is a file
    if not os.path.isfile(target_file):
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

    # STEP 3: WRITE FILE CONTENT
    # =========================

    try:
        # Open the file in write mode with UTF-8 encoding
        with open(target_file, "w", encoding="utf-8") as file:
            # Write the content to the File
            file.write(content)

        # Return a success message
        return f'Successfully wrote to "{file_path}" {len(content)} characters written'

    except OSError as e:
        # ERROR HANDLING: Catch any operating system errors
        # OSError covers many common issues:
        # - PermissionError: User doesn't have permission to write file_path
        # - FileNotFoundError: File was deleted between validation and writing
        # - IsADirectoryError: Path changed from file to directory
        # Always return a string (never raise exceptions) so the LLM can handle errors gracefully
        return f"Error: {e}"

    except Exception as e:
        # Catch any other unexpected errors
        return f"Error: An unexpected error occurred while writing to {file_path}: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="The path to the file to write."
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The content to write to the file."
            ),
        },
        required=["file_path", "content"],
    ),
)
