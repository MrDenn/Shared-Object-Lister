import unittest
import os
import subprocess
import tempfile
from src.parser import parse_shared_object_file
from src.cli import sort_criteria

TEST_C_CODE = """
// global_function should be printed with the STB_GLOBAL bind
// Should appear as ['global_function', 'STB_GLOBAL'] in the output
void global_function() { }

// a_funciton should be printed above z_funciton
void z_function() { }
void a_function() { }

// weak_function should be printed with the STB_WEAK bind
// Should appear as ['weak_function', 'STB_WEAK'] in the output
void __attribute__((weak)) weak_function() { }

// local_function should not be printed
// Would appear as ['', 'STB_LOCAL'] if not filtered properly
static void local_function() { }
"""


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Temporary directory is created for compilation to take place
        self.tmp_dir = tempfile.TemporaryDirectory()

        # Write the C code seen above to .c file
        c_path = os.path.join(self.tmp_dir.name, 'test.c')
        with open(c_path, 'w') as f:
            f.write(TEST_C_CODE)

        # Generate .so shared object file path
        self.so_path = os.path.join(self.tmp_dir.name, 'test.so')

        # Use GCC to compile the C code into a .so shared object file
        subprocess.check_call(
            ['gcc', '-shared', '-fPIC', c_path, '-o', self.so_path]
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_integration(self):
        # Open resulting .so file to test its output
        with open(self.so_path, 'rb') as file:
            funcs = parse_shared_object_file(file)

            # Global functions should be present in returned array
            self.assertIn(['global_function', 'STB_GLOBAL'], funcs)
            # Weak functions should be present in returned array
            self.assertIn(['weak_function', 'STB_WEAK'], funcs)
            # No local functions should be present in returned array
            self.assertNotIn(['', 'STB_LOCAL'], funcs)

            # Test correctness of sorting algorithm in cli.py
            funcs.sort(key=sort_criteria)

            # Set indices to reflect position of these functions in sorted array
            index_a = funcs.index(['a_function', 'STB_GLOBAL'])
            index_z = funcs.index(['z_function', 'STB_GLOBAL'])
            # Index of 'a_function' should be less than index of 'b_function'
            self.assertLess(index_a, index_z, "a_function should be printed above z_function")


if __name__ == '__main__':
    unittest.main()
