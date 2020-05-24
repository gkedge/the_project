from the_project import Module0

print("Execute The Project.")


def main_reusable_func():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print(main_reusable_func())
