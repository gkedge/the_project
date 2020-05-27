"""
A simple __main__ to access references in the the_package
"""

from runtime_syspath import print_syspath

import the_project

print("Execute The Project.")


def main_reusable_func() -> str:
    """
    A reusable function that could be run from outside this module.
    :return: a string indicating what could be run from th e
    """
    the_prog_mod0 = the_project.Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print_syspath(sort=False)
    print(main_reusable_func())
