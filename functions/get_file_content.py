import os
import os.path
import sys

from google.genai import types

from config import MAX_CHARACTERS

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_file_content(working_directory, file_path):
    """
    Get the content of a file within a specified working directory.

    This function is designed to be safe for LLM agents by:
    1. Preventing access outside the working directory (security)
    2. Always returning strings (LLM-friendly)
    3. Handling all errors gracefully
    4. Truncating long files to prevent memory issues

    Args:
        working_directory (str): The base directory that acts as a security boundary
        file_path (str): The path to the file to read within the working directory

    Returns:
        str: Either the file content (possibly truncated) or an error message
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
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # STEP 2: FILE VALIDATION
    # =========================

    # Check if the path actually exists and is a file
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" is not a file'

    # STEP 3: READ FILE CONTENT
    # =========================

    try:
        # Open the file in read mode with UTF-8 encoding
        # This handles text files properly across different systems
        with open(target_file, "r", encoding="utf-8") as file:
            # Read the entire content of the file
            content = file.read()

        # Check if the file is longer than our character limit
        # If so, truncate it and add a message
        if len(content) > MAX_CHARACTERS:
            truncated_content = content[:MAX_CHARACTERS]
            truncation_message = (
                f'\n\n[File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
            )
            return truncated_content + truncation_message
        else:
            # Return the full content if it's within limits
            return content

    except UnicodeDecodeError as e:
        # Handle files that can't be read as text (binary files, wrong encoding)
        return "Error: Cannot read file as text - it may be a binary file or have unsupported encoding"

    except OSError as e:
        # ERROR HANDLING: Catch any operating system errors
        # OSError covers many common issues:
        # - PermissionError: User doesn't have permission to read file
        # - FileNotFoundError: File was deleted between validation and reading
        # - IsADirectoryError: Path changed from file to directory
        # Always return a string (never raise exceptions) so the LLM can handle errors gracefully
        return f"Error: {e}"

    except Exception as e:
        # Catch any other unexpected errors
        return f"Error: An unexpected error occurred while reading {file_path}"

    # Note: We don't need a general except clause because:
    # 1. OSError covers most file system operations
    # 2. UnicodeDecodeError covers text encoding issues
    # 3. Our code doesn't do anything that could raise other exceptions
    # 4. If something unexpected happens, it's better to let it bubble up for debugging


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="The path to the file to read."
            ),
        },
    ),
)
