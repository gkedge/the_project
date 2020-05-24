import sys
from pathlib import Path

from runtime_syspath import print_syspath

if __name__ != "__main__":
    SRC_PATH = Path(__file__).parent
    SRC_DIR_STR = str(SRC_PATH.absolute())
    if SRC_DIR_STR not in sys.path:
        sys.path.append(SRC_DIR_STR)
        print_syspath(sort=False)
else:
    print_syspath(sort=False)

# pylint: disable=import-error

# Why is Pycharm being dumb here? Answered with a Q on __main__ tests below...
from the_project import Module0

# pylint: disable=import-error

print("Execute The Project.")


# On your way down, here's a hint: the name of this function...
def reusable_function():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


# What does this if-test do?
if __name__ == "__main__":
    print(reusable_function())
