import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import MODEL, SYSTEM_PROMPT
        # Import the call_function and available_functions from the new module
    from call_function import call_function, available_functions

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    # Parse command line arguments
    verbose_mode = "--verbose" in sys.argv
    # Get the last argument that's not --verbose
    user_prompt = None
    for arg in reversed(sys.argv[1:]):
        if arg != "--verbose":
            user_prompt = arg
            break

    if not user_prompt:
        print("Error: No user prompt provided")
        return

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    if not user_prompt:
        Exception("exit code 1")
    if verbose_mode:
        print(f" User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

    # Check if there are function calls in the response (run in both verbose and non-verbose modes)
    if hasattr(response, "candidates") and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, "content") and candidate.content:
            for part in candidate.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    # Use the new call_function to handle the function call
                    function_call_result = call_function(part.function_call, verbose=verbose_mode)

                    # Verify the response structure
                    if not hasattr(function_call_result, 'parts') or not function_call_result.parts:
                        raise Exception("Invalid function call result structure")

                    if not hasattr(function_call_result.parts[0], 'function_response'):
                        raise Exception("Missing function_response in result")

                    if not hasattr(function_call_result.parts[0].function_response, 'response'):
                        raise Exception("Missing response in function_response")

                    # Always show the function result, not just in verbose mode
                    response_data = function_call_result.parts[0].function_response.response
                    if isinstance(response_data, dict):
                        if "result" in response_data:
                            print(f"Function result: {response_data['result']}")
                        elif "error" in response_data:
                            print(f"Function error: {response_data['error']}")
                    else:
                        print(f"Function result: {response_data}")

                    # Also show in verbose mode with the -> format
                    if verbose_mode:
                        print(f"-> {response_data}")


if __name__ == "__main__":
    main()
