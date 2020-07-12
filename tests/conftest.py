import sys
from pathlib import Path

import pytest
from runtime_syspath import print_syspath

sys.dont_write_bytecode = True

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).absolute().parent.parent
assert str(PROJECT_PATH / 'src') not in sys.path
sys.path.append(str(PROJECT_PATH / 'src'))
print_syspath(sort=False)

from the_project import Module0


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
