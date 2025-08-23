#!/usr/bin/env python3
"""
Test file for both write_file and run_python_file functions.
This file demonstrates all the expected behaviors and outputs.
"""

# Import our functions from the functions subdirectory
from functions.write_file import write_file
from functions.run_python import run_python_file


def run_tests():
    """
    Run all tests for both functions.
    Each test demonstrates a different aspect of the functions' behavior.
    """

    print("🧪 TESTING write_file FUNCTION")
    print("=" * 50)

    # TEST 1: Write to existing file (calculator/lorem.txt)
    print("\n📝 TEST 1: Writing to existing file (calculator/lorem.txt)")
    print("-" * 40)
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result for 'lorem.txt':")
    print(result)
    print("\nExpected: Success message about writing to lorem.txt")

    # TEST 2: Write to new file in subdirectory (calculator/pkg/morelorem.txt)
    print(
        "\n📝 TEST 2: Writing to new file in subdirectory (calculator/pkg/morelorem.txt)"
    )
    print("-" * 40)
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for 'pkg/morelorem.txt':")
    print(result)
    print("\nExpected: Success message about writing to pkg/morelorem.txt")

    # TEST 3: Security test - try to write outside working directory (should return error)
    print("\n🚫 TEST 3: Security check - trying to write to /tmp/temp.txt")
    print("-" * 40)
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for '/tmp/temp.txt':")
    print(result)
    print("\nExpected: Error message about being outside permitted working directory")

    print("\n🧪 TESTING run_python_file FUNCTION")
    print("=" * 50)

    # TEST 4: Run calculator/main.py without arguments (should print usage instructions)
    print("\n🐍 TEST 4: Running calculator/main.py without arguments")
    print("-" * 40)
    result = run_python_file("calculator", "main.py")
    print("Result for 'main.py' (no args):")
    print(result)
    print("\nExpected: Calculator's usage instructions")

    # TEST 5: Run calculator/main.py with arguments ["3 + 5"] (should calculate result)
    print("\n🐍 TEST 5: Running calculator/main.py with arguments ['3 + 5']")
    print("-" * 40)
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for 'main.py' with args ['3 + 5']:")
    print(result)
    print("\nExpected: Calculator result for 3 + 5")

    # TEST 6: Run calculator/tests.py (should run the test file)
    print("\n🐍 TEST 6: Running calculator/tests.py")
    print("-" * 40)
    result = run_python_file("calculator", "tests.py")
    print("Result for 'tests.py':")
    print(result)
    print("\nExpected: Output from running the test file")

    # TEST 7: Security test - try to run ../main.py (should return error)
    print("\n🚫 TEST 7: Security check - trying to run ../main.py")
    print("-" * 40)
    result = run_python_file("calculator", "../main.py")
    print("Result for '../main.py':")
    print(result)
    print("\nExpected: Error message about being outside permitted working directory")

    # TEST 8: File not found - try to run non-existent file (should return error)
    print("\n❌ TEST 8: File not found - trying to run nonexistent.py")
    print("-" * 40)
    result = run_python_file("calculator", "nonexistent.py")
    print("Result for 'nonexistent.py':")
    print(result)
    print("\nExpected: Error message about file not found")

    print("\n🧪 TESTING get_files_info FUNCTION")
    print("=" * 50)

    # TEST 9: List files in root directory
    print("\n📁 TEST 9: Listing files in root directory")
    print("-" * 40)
    from functions.get_file_info import get_files_info

    result = get_files_info(".", ".")
    print("Result for root directory:")
    print(result)
    print("\nExpected: List of files and directories in the current directory")

    # TEST 10: List files in pkg directory
    print("\n📁 TEST 10: Listing files in pkg directory")
    print("-" * 40)
    result = get_files_info(".", "pkg")
    print("Result for 'pkg' directory:")
    print(result)
    print("\nExpected: List of files and directories in the pkg directory")

    print("\n🧪 TESTING FUNCTION CALLING WITH LLM")
    print("=" * 50)

    # TEST 11: Test LLM function calling for reading file contents
    print("\n📖 TEST 11: LLM function call - read the contents of main.py")
    print("-" * 40)
    print("Expected: get_file_content({'file_path': 'main.py'})")
    print("Note: This test demonstrates the LLM's ability to choose the right function")

    # TEST 12: Test LLM function calling for writing files
    print("\n✍️ TEST 12: LLM function call - write 'hello' to main.txt")
    print("-" * 40)
    print("Expected: write_file({'file_path': 'main.txt', 'content': 'hello'})")
    print("Note: This test demonstrates the LLM's ability to choose the right function")

    # TEST 13: Test LLM function calling for running Python files
    print("\n🐍 TEST 13: LLM function call - run main.py")
    print("-" * 40)
    print("Expected: run_python_file({'file_path': 'main.py'})")
    print("Note: This test demonstrates the LLM's ability to choose the right function")

    # TEST 14: Test LLM function calling for listing directory contents
    print("\n📁 TEST 14: LLM function call - list the contents of the pkg directory")
    print("-" * 40)
    print("Expected: get_files_info({'directory': 'pkg'})")
    print("Note: This test demonstrates the LLM's ability to choose the right function")

    print("\n" + "=" * 50)
    print("✅ ALL TESTS COMPLETED!")
    print("\n💡 TROUBLESHOOTING TIPS:")
    print("1. If you get import errors, make sure you're running from the project root")
    print("2. If paths don't work, check that the 'calculator' directory exists")
    print("3. If you get permission errors, check file/directory permissions")
    print("4. Compare your output with the expected results above")
    print("\n🎯 EXPECTED OUTPUT CONTAINS:")
    print("- Success messages for valid file writes (with character counts)")
    print("- Error messages for security violations")
    print("- Calculator usage instructions from main.py")
    print("- Calculator result for 3 + 5")
    print("- Test file execution output")
    print("- Error messages for security violations and missing files")


if __name__ == "__main__":
    # This ensures the tests only run when the file is executed directly
    # (not when imported as a module)
    run_tests()
