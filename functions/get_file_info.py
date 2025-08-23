import os


def get_files_info(working_directory, directory="."):
    """
    Get information about files and directories within a specified working directory.

    This function is designed to be safe for LLM agents by:
    1. Preventing access outside the working directory (security)
    2. Always returning strings (LLM-friendly)
    3. Handling all errors gracefully

    Args:
        working_directory (str): The base directory that acts as a security boundary
        directory (str): Relative path within working_directory to list (defaults to current ".")

    Returns:
        str: Either a formatted list of files/directories or an error message
    """

    # STEP 1: PATH CONSTRUCTION AND VALIDATION
    # ==========================================

    # Convert working directory to absolute path first (cleaner approach)
    abs_working_dir = os.path.abspath(working_directory)

    # Join paths and convert to absolute path immediately (instructor's approach)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # SECURITY CHECK: Ensure the requested path stays within working directory boundaries
    # This prevents the LLM from accessing files outside its permitted area
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # STEP 2: DIRECTORY VALIDATION
    # =============================

    # Check if the path actually exists and is a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    # STEP 3: DIRECTORY LISTING AND PROCESSING
    # =========================================

    try:
        # Get a list of all items (files and directories) in the specified directory
        files_info = []

        # Process each item in the directory
        for filename in os.listdir(target_dir):
            # Construct the full path to this specific item
            filepath = os.path.join(target_dir, filename)

            # Determine if this item is a directory or a file
            is_dir = os.path.isdir(filepath)

            # FORMATTING: Create the output line according to the specified format
            # The format must be exactly: "- filename: file_size=X bytes, is_dir=Y"
            if is_dir:
                # For directories, we can't use os.path.getsize() reliably
                # Some systems return different values for directories
                # So we'll use a descriptive string instead
                line = f"- {filename}: file_size=directory, is_dir=True"
            else:
                # For files, get the actual size in bytes
                # os.path.getsize() returns the file size in bytes
                file_size = os.path.getsize(filepath)
                line = f"- {filename}: file_size={file_size} bytes, is_dir=False"

            # Add this formatted line to our collection
            files_info.append(line)

        # STEP 4: ASSEMBLE FINAL OUTPUT
        # ==============================

        # Join all the individual lines together with newline characters
        # This creates a multi-line string that's easy for the LLM to read
        return "\n".join(files_info)

    except OSError as e:
        # ERROR HANDLING: Catch any operating system errors
        # OSError covers many common issues:
        # - PermissionError: User doesn't have permission to read directory
        # - FileNotFoundError: Directory was deleted between validation and listing
        # - NotADirectoryError: Path changed from directory to file
        # Always return a string (never raise exceptions) so the LLM can handle errors gracefully
        return f"Error: {e}"

    # Note: We don't need a general except clause because:
    # 1. OSError covers most file system operations
    # 2. Our code doesn't do anything that could raise other exceptions
    # 3. If something unexpected happens, it's better to let it bubble up for debugging


from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
