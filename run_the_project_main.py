from module0 import Module0

print("Execute The Project.")


def reusable_function():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print(reusable_function())
