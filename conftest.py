import sys
from pathlib import Path

import pytest
from runtime_syspath import print_syspath

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).parent.absolute()
SRC_DIR_STR = str(PROJECT_PATH / 'src')
if SRC_DIR_STR not in sys.path:
    sys.path.append(SRC_DIR_STR)
    print_syspath(sort=False)

# pylint: disable=import-error
from the_project import Module0

# pylint: enable=import-error


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
