from typing import BinaryIO
from elftools.elf.elffile import ELFFile

# Libraries (.so files) I used for testing:
# /usr/lib/aarch64-linux-gnu/libm.so.6
# /usr/lib/aarch64-linux-gnu/libmpfr.so.6.2.2
# /usr/lib/aarch64-linux-gnu/libanl.so.1

def parse_shared_object_file(file: BinaryIO) -> list[tuple[str, str]]:
    exported_functions = [] # array to contain function names

    elf = ELFFile(file)                          # feeding ELF tools the file
    section = elf.get_section_by_name('.dynsym') # only look in the Dynamic Symbol Table

    for symbol in section.iter_symbols():
        is_function = symbol['st_info']['type'] == 'STT_FUNC'
        is_visible = symbol['st_info']['bind'] in ('STB_WEAK', 'STB_GLOBAL')
        is_defined_here = symbol['st_shndx'] != 'SHN_UNDEF'

        if is_function and is_visible and is_defined_here:
            binding = symbol['st_info']['bind']
            exported_functions.append((symbol.name, binding))

    return exported_functions

