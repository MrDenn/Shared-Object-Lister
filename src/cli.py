import sys
from src.parser import parse_shared_object_file

def main():
    file_path = input("Type the path to the .so file: ")

    try:
        functions = parse_shared_object_file(file_path)
        for func in functions:
            print_function(func)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse file. {e}", file=sys.stderr)
        sys.exit(1)

def print_function(function):
    print(f"Name: {function[0]:<25} Visibility: {function[1]}")
