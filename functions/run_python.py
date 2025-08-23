import subprocess
import sys
import os
import os.path
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    """
    Run a Python file within a specified working directory.

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
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # STEP 2: FILE VALIDATION
    # =========================

    # Check if the path actually exists and is a file
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'

    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # STEP 3: RUN PYTHON FILE
    # ========================

    try:
        # Prepare command with arguments
        cmd = ["python", target_file]
        if args:
            cmd.extend(args)

        # Use subprocess.run to run the Python file
        result = subprocess.run(
            cmd, capture_output=True, timeout=30, cwd=working_directory, text=True
        )

        # Format output according to assignment requirements
        output_parts = []

        # Add stdout if present
        if result.stdout.strip():
            output_parts.append(f"STDOUT: {result.stdout}")

        # Add stderr if present
        if result.stderr.strip():
            output_parts.append(f"STDERR: {result.stderr}")

        # Add process exit code if non-zero
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # If no output was produced, return the specified message
        if not output_parts:
            return "No output produced."

        # Join all output parts with newlines
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: executing Python file: timeout after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
