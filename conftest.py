import pytest
from runtime_syspath import print_syspath

# pylint: disable=import-error
from src.the_project.module0 import Module0

# PROJECT_DIR = Path(__file__).parent
# sys.path.append(str(PROJECT_DIR / 'src'))

# pylint: enable=import-error

print_syspath(sort=False)


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
