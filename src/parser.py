from elftools.elf.elffile import ELFFile

# Libraries (.so files) I used for testing:
# /usr/lib/aarch64-linux-gnu/libm.so.6
# /usr/lib/aarch64-linux-gnu/libmpfr.so.6.2.2
# /usr/lib/aarch64-linux-gnu/libanl.so.1

def parse_shared_object_file(file_path):

    with open(file_path, 'rb') as file:
        functions = [] # array to contain function names

        elf = ELFFile(file) # feeding Elf the file

        section = elf.get_section_by_name('.dynsym') # only look in the Dynamic Symbol Table

        for symbol in section.iter_symbols():
            name = symbol.name               # name of symbol
            type = symbol['st_info']['type'] # type of symbol
            bind = symbol['st_info']['bind'] # visibility of symbol
            section = symbol['st_shndx']     # location of symbol in library (if SHN_UNDEF, then borrowed)

            print(f"Name: {name:<32} Type: {type:<13} Binding: {bind:<13} Section: {symbol['st_shndx']}")


