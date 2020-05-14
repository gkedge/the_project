import sys
from pathlib import Path

import pytest
from runtime_syspath import print_syspath

PROJECT_DIR = Path(__file__).parent
sys.path.append(str(PROJECT_DIR / 'src'))

# pylint: disable=import-error
from the_project.module0 import Module0

# pylint: enable=import-error

print_syspath(sort=False)


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
