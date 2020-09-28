import atexit
import os
import sys
from pathlib import Path

from runtime_syspath import print_syspath

sys.dont_write_bytecode = True

if os.getenv('SYSPATH_SLEUTH_KILL') is None:
    from runtime_syspath import syspath_sleuth

    syspath_sleuth.inject_sleuth()


    def uninstall_syspath_sleuth():
        syspath_sleuth.uninstall_sleuth()


    atexit.register(uninstall_syspath_sleuth)

import pytest

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).parent.parent.absolute()
assert str(PROJECT_PATH / "src") not in sys.path
sys.path.append(str(PROJECT_PATH / "src"))
print_syspath(sort=False)

from the_project import Module0


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
