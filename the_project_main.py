# PROJECT_DIR = Path(__file__).parent
# sys.path.append(str(PROJECT_DIR / 'src'))

# pylint: disable=import-error
from src.the_project.module0 import Module0

# pylint: enable=import-error

print("Execute The Project.")


def main():
    the_prog_mod0: Module0 = Module0()
    return f'Exercise {the_prog_mod0.func0()} on class {the_prog_mod0}.'


if __name__ == "__main__":
    print(main())
