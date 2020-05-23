import sys
from pathlib import Path

from runtime_syspath import print_syspath

PROJECT_DIR = Path(__file__).parent
sys.path.append(str(PROJECT_DIR / 'src'))

# pylint: disable=import-error
from the_project import Module0  # noqa

# pylint: enable=import-error

print_syspath(sort=False)

print("Execute The Project.")


def main():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print(main())
