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
        functions = parse_shared_object_file(args.file_path)
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
