import sys
from pathlib import Path

from runtime_syspath import print_syspath

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).absolute().parent.parent
assert str(PROJECT_PATH / 'src') not in sys.path  # noqa
sys.path.append(str(PROJECT_PATH / 'src'))

print_syspath(sort=False)

from run_the_project_main import main_reusable_func  # noqa

if __name__ == "__main__":
    print(main_reusable_func())
