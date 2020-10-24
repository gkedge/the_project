import sys
from pathlib import Path

import pytest
from runtime_syspath import print_syspath, syspath_sleuth

sys.dont_write_bytecode = True

if syspath_sleuth.is_install_on_import():
    print("SysPathSleuth activated!")

print_syspath(sort=False)

PROJECT_PATH = Path(__file__).parent.parent.absolute()
assert str(PROJECT_PATH / "src") not in sys.path
sys.path.append(str(PROJECT_PATH / "src"))
print_syspath(sort=False)

from the_project import Module0


# def persist_path_at_exit():
#     persist_syspath(force_pth_dir_creation=True)
#
#
# atexit.register(persist_path_at_exit)


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
