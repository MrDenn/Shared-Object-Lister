import argparse
import sys
from src.parser import parse_shared_object_file

def main() -> None:
    """
    Entry point for the CLI application.

    Parses command-line arguments, reads the specified shared object file,
    and prints all exported function names to stdout. Handles errors gracefully
    with informative messages sent to stderr.

    Returns:
        None

    Exits:
        sys.exit(0): On successful completion
        sys.exit(1): If the specified file is not found
        sys.exit(2): If other unexpected errors occur
    """

    parser = argparse.ArgumentParser(
        prog="Shared Object Lister",
        description="List available native functions from a Linux .so file.")
    parser.add_argument(
        "file_path",
        help="Absolute path to the shared object (.so) file")
    args = parser.parse_args()

    try:
        # Open .so file at the given file path
        with open(args.file_path, 'rb') as file:
            # Retrieve function symbols from parser
            functions = parse_shared_object_file(file)
            # Sort function symbols
            functions.sort(key=sort_criteria)
            # Get max length among symbol names for formatting
            max_len = get_max_function_name_length(functions)
            # Print function symbols, formatted appropriately
            print_functions(functions, max_len)
        sys.exit(0)
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse file. {e}", file=sys.stderr)
        sys.exit(2)

def sort_criteria(function: tuple[str, str]) -> tuple[int, str]:
    """
    Helper function to determine sorting order.

    Priority for sorting are as follows:
    - First, binding of the symbol (GLOBAL first, WEAK second)
    - Then, name of the symbol (in alphabetical order)

    Args:
        function_name tuple[str, str]: The function name and visibility.

    Returns:
        str: The lowercased name for case-insensitive sorting.
    """
    name, binding = function

    # GLOBAL shold be first as the higher visibility level
    if binding == 'STB_GLOBAL':
        priority = 0
    # WEAK should be second, as it's still public, but less so
    elif binding == 'STB_WEAK':
        priority = 1
    # Anything else shouldn't be possible, but added for anomalies
    else:
        priority = 2

    # Sort primarily by visibility, then by function name
    return (priority, name)

def get_max_function_name_length(functions: list[tuple[str, str]]) -> int:
    """
    Helper function to determine the maximum function name length in the input.

    Performs a linear pass through the input array and looks for the maximum name length.

    Args:
        functions: List of tuples containing function name and its visibility.

    Returns:
        int: The maximum function name length.

    """
    max_name_length = 0

    # Loop through all function symbols
    for function in functions:
        # Compare stored max length with current function name length
        if len(function[0]) > max_name_length:
            max_name_length = len(function[0])

    return max_name_length

def print_functions(functions: list[tuple[str, str]], max_name_length: int) -> None:
    """
    Helper function to neatly print the given function names and their visibility.

    Args:
        functions:        List of tuples containing function name and its visibility.
        max_name_length:  The maximum function name length.

    Returns:
        None
    """
    for function in functions:
        print(f"Name: {function[0]:<{max_name_length}} | Visibility: {function[1]}")
