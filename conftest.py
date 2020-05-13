import pytest
from runtime_syspath import print_syspath

from the_project.module0 import Module0

print_syspath(sort=False)


@pytest.fixture
def fixture0() -> Module0:
    return Module0()
