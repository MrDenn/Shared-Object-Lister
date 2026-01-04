from typing import BinaryIO
from elftools.elf.elffile import ELFFile

# Libraries (.so files) I used for testing:
# /usr/lib/aarch64-linux-gnu/libm.so.6
# /usr/lib/aarch64-linux-gnu/libmpfr.so.6.2.2
# /usr/lib/aarch64-linux-gnu/libanl.so.1

def parse_shared_object_file(file: BinaryIO) -> list[tuple[str, str]]:
    """
    Parses the given object file and returns a list of exported function symbols.

    Opens an ELF binary file and extracts all globally visible function symbols
    from the dynamic symbol table (.dynsym). Filters symbols to include only
    those that are:
    - Of type STT_FUNC (function)
    - With binding STB_GLOBAL or STB_WEAK (globally visible)
    - Defined in this file (not imported from other libraries)

    Args:
        file (BinaryIO): A file-like object opened in binary mode containing
                         valid ELF data.

    Returns:
        list[tuple[str, str]]: Sorted list of (symbol_name, binding_type) tuples
                               for all exported functions.
    """

    exported_functions = [] # array to contain function names

    elf = ELFFile(file)                          # feeding ELF tools the file
    section = elf.get_section_by_name('.dynsym') # only look in the Dynamic Symbol Table

    for symbol in section.iter_symbols():
        # Check if symbol is a function
        is_function = symbol['st_info']['type'] == 'STT_FUNC'
        # Check if symbol is globally (or weakly) visible
        is_visible = symbol['st_info']['bind'] in ('STB_WEAK', 'STB_GLOBAL')
        # Check if symbol is defined in this file (and not imported)
        is_defined_here = symbol['st_shndx'] != 'SHN_UNDEF'

        if is_function and is_visible and is_defined_here:
            binding = symbol['st_info']['bind']
            exported_functions.append((symbol.name, binding))

    return exported_functions

