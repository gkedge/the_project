from pathlib import Path

import pytest


def test_can_test_case_import_from_root_dir():
    print(f"\n\nFrom this current working directory: {Path.cwd()}")
    try:
        import can_test_case_import  # in root directory...

        print("Test case imported a module from the root directory?\n"
              "Strange... since I am not augmenting sys.path... Promise!")

        pytest.fail('Why can I import from project root directory?')
    except ImportError as e:
        print("\t... you cannot import 'can_test_case_import' in project root directory. Whew.")


if __name__ == "__main__":
    test_can_test_case_import_from_root_dir()
