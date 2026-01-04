# Shared Object Lister

A lightweight command-line tool that reads the binary data inside of Shared Object (.so) files and lists all available
native functions in the given shared object.

## Features

- **ELF Parsing**: directly parses binary `.so` files using `pyelftools` (without reliance on system `nm` or `objdump`)
- **Comprehensive event reporting**: workflow queuing/starts/completions, job starts/completions, step starts/completions
- **Sorted Output**: Displays function names alphabetically for easy reading.
- **Robust Testing**: Includes integration tests that compile real C code on-the-fly to verify parser accuracy.

## Output Format

Each event is printed as a single line with fixed-width columns for easy parsing and log integration:

```
Name: [function name]   Visibility: [funciton visibiility level] 
```

### Example Output

```
Name: exp                       Visibility: STB_GLOBAL
Name: fmod                      Visibility: STB_GLOBAL
Name: log                       Visibility: STB_GLOBAL
Name: pow                       Visibility: STB_GLOBAL
Name: atan                      Visibility: STB_WEAK
Name: cos                       Visibility: STB_WEAK
Name: sin                       Visibility: STB_WEAK
Name: sqrt                      Visibility: STB_WEAK
Name: tan                       Visibility: STB_WEAK
Name: trunc                     Visibility: STB_WEAK
```

## Quick Start

### Prerequisites

- Python 3.12
- Pip 3 to install the necessary dependencies
- Absolute path of .so file to be analyzed
- GCC (Only if running the test suite)
  - On my machine, the test suite worked only on a Docker container with Linux
  - I was not able to get the test script running on any system other than a Docker container with Linux
  - This might work if GCC 

### Running

```bash
# On a clean machine running Linux/Windows/MacOS:
cd [path to project root]
pip3 install -r requirements.txt
python3 main.py [absolute path to .so file]
```
```bash
# If you already have all the prerequisites installed
python3 [path to main.py] [absolute path to .so file]
```

### Running Testing Suite

```bash
# On a Linux machine with all prerequisites installed:
python3 [path to test_integration.py]
```
```bash
# In a Docker container constructed from the Dockerfile in this repository:
/usr/local/bin/python3 /opt/project/tests/test_integration.py
```

## Behavioral Details

### Retrieval of .so file

- Path to .so file is passed through script parameters/arguments
- The CLI script retrieves the arguments and opens the file
- The CLI script passes the retrieved file object to the parser script

### Parsing of .so file

- When the parser script receives the file object, it hands it to the pyelftools parser
- pyelftools parser discards everything except the Dynamic Symbol Table and fragments it into 'symbols'

### Filtering of non-desired symbols

- For each symbol, three checks have to be passed before it's added to the output list:
  - The symbol has to represent a function
  - The symbol has to be accessible from the outside (not LOCAL visibility)
  - The symbol has to be defined within the given .so file (and not a reference to another shared object)

### Sorting of the output

- When the list symbols is returned by the parser to the CLI script, it's sorted using a custom sort criteria function such that:
  - Symbols are primarily sorted by their visibility: GLOBAL first, WEAK second
  - The remaining order is then made alphabetical by symbol name

### Dynamic formatting of output 

- In the sorted list of symbols, the maximum symbol name length
- All symbols are then printed into the console in a loop
  - Each symbol/function name is formatted to the maximum symbol name length found earlier
  - Then, the visibility of the corresponding symbol is printed after a separator

## Design Decisions

### Using 'pyelftools' instead of system commands

**Decision**: External library pyelftools is used to parse bytecode of .so files instead of calling system commands like 'nm' or 'objdump' and catching their console output.
- **Rationale**: parsing bytecode within the application allows for more flexibility down the road and (in theory) should be faster.
- **Tradeoff**: this requires all users of this utility to install a dependency instead of the project being fully self-contained.

### Sorting the output

**Decision**: The output from the pyelftools parser is sorted first, primarily by the visibility value, and after that the remaining order is determined alphabetically by function name.
- **Rationale**: sorting by visibility allows to clearly see which functions in the shared object were made to be accessible and visible (typically GLOBAL), and which are accessible for other reasons (typically WEAK).

### Compiling a fresh .so file for testing

**Decision**: The test suite contains a fragment of C code, which is compiled every time it (the resulting .so file) needs to be used for testing. 
- **Rationale**: having the C code in text form, rather than baked into bytecode allows for much easier adjustment of the .so that the tests are run for.
- **Tradeoff**: the use of GCC for compilation means that the test suite works well mostly on Linux, and running it on other operating systems is much more challenging.

---

## Known Limitations

- **Dropped function details**: Not all useful fields are exposed in the Dynamic Symbol Table, so not all available information is retrieved from the .so bytecode.
- **Testing dependent on GCC**: Queued runs are only queried from the last 24 hours, which may not always be caused by a stale workflow run.

## Possible Future Enhancements

- Full analysis of .so bytecode using reverse engineering tools like IDA Pro or Ghidra could allow to extract:
  - Function parameters
  - Parameter types
  - Return types
- Implement testing based on baked-in bytecode instead of compiling C or C++ code on-the-fly, which would remove GCC as a dependency for testing.

## Architecture Overview

```
Shared-Object-Lister/
├── src/
│   ├── parser.py       # Core logic for ELF parsing, symbol extraction, and symbol filtering
│   └── cli.py          # Command-line interface and sorting logic
├── tests/
│   └── test_parser.py  # Integration tests (compiles sample C code to verify logic)
├── main.py             # Entry point script
├── requirements.txt    # Project dependencies
├── Dockerfile          # Docker configuration
└── README.md           # Project documentation

```

---

**Last updated**: January 2026
**Python Version**: 3.12
**Dependencies**: ELFTools 0.32, GCC (for testing)
