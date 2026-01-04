import argparse
import sys
from src.parser import parse_shared_object_file

def main():
    parser = argparse.ArgumentParser(
        prog="Shared Object Lister",
        description="List available native functions from a Linux .so file.")
    parser.add_argument(
        "file_path",
        help="Absolute path to the shared object (.so) file")
    args = parser.parse_args()

    try:
        with open(args.file_path, 'rb') as file:
            functions = parse_shared_object_file(file)
            functions.sort(key=sort_criteria)
            max_len = get_max_function_name_length(functions)
            print_functions(functions, max_len)
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse file. {e}", file=sys.stderr)
        sys.exit(1)

def sort_criteria(function):
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

def get_max_function_name_length(functions):
    max_name_length = 0

    for function in functions:
        if len(function[0]) > max_name_length:
            max_name_length = len(function[0])

    return max_name_length

def print_functions(functions, max_name_length):
    for function in functions:
        print(f"Name: {function[0]:<{max_name_length}} | Visibility: {function[1]}")
