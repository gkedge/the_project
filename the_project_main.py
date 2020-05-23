from the_project import Module0
from runtime_syspath import print_syspath

print_syspath(sort=False)

print("Execute The Project.")


def main():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print(main())
