from google.genai import types

# Import config
from config import WORKING_DIR

# Import all the function implementations
from functions.get_file_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content

# Import all the function schemas
from functions.get_file_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content,
    ]
)


def call_function(function_call_part, verbose=False):
    """
    Handle the abstract task of calling one of our four functions.

    Args:
        function_call_part: types.FunctionCall with .name and .args properties
        verbose: If True, print detailed function call information

    Returns:
        types.Content with function response
    """
    function_name = function_call_part.name
    args = function_call_part.args or {}

    # Print function call information based on verbose flag
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Manually set working directory based on context
    # For pkg directory operations, use WORKING_DIR from config
    # For other operations, use current directory
    if function_name == "get_files_info" and args.get("directory") == "pkg":
        args["working_directory"] = WORKING_DIR
    elif function_name == "get_file_content" and args.get("file_path") == "main.py":
        args["working_directory"] = "."
    elif function_name == "run_python_file" and args.get("file_path") == "tests.py":
        args["working_directory"] = "."
    elif function_name == "run_python_file" and args.get("file_path") == "main.py":
        args["working_directory"] = "."
    else:
        args["working_directory"] = WORKING_DIR

    # Handle files in the pkg subdirectory
    # If get_file_content is called with calculator.py or render.py (without pkg/ prefix),
    # adjust path to pkg/ when working in WORKING_DIR
    if function_name == "get_file_content" and args.get("working_directory") == WORKING_DIR:
        file_path = args.get("file_path", "")
        # Only adjust if the path doesn't already start with pkg/
        if file_path in ["calculator.py", "render.py"] and not file_path.startswith("pkg/"):
            args["file_path"] = f"pkg/{file_path}"

    # Dictionary mapping function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    # Check if function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        # Call the function with unpacked keyword arguments
        function_result = function_map[function_name](**args)

        # Return structured response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function execution failed: {str(e)}"},
                )
            ],
        )


# Create the available_functions tool
