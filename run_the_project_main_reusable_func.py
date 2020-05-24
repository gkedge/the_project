import sys
from pathlib import Path

from runtime_syspath import print_syspath

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).parent.absolute()
SRC_DIR_STR = str(PROJECT_PATH / 'src')
if SRC_DIR_STR not in sys.path:
    sys.path.append(SRC_DIR_STR)
    print_syspath(sort=False)

# pylint: disable=import-error
from run_the_project_main import main_reusable_func

# pylint: enable=import-error

if __name__ == "__main__":
    print(main_reusable_func())
