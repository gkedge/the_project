"""
A simple __main__ to access references in the the_package
"""
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

# Why is Pycharm/pylint being dumb here? Answered with a Q on __main__ tests below...
import the_project

print("Execute The Project.")


# On your way down, here's a hint: the name of this function...
def main_reusable_func() -> str:
    """
    A reusable function that could be run from outside this module.
    :return: a string indicating what could be run from th e
    """
    the_prog_mod0 = the_project.Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


# What does this if-test do?
if __name__ == "__main__":
    print(main_reusable_func())
