from pathlib import Path

from _pytest.fixtures import SubRequest

from common import mkdir_p


def test_mkdir_p(request: SubRequest):
    def finalize_test():
        Path('tmper').rmdir()

    request.addfinalizer(finalize_test)
    mkdir_p('tmper')

    assert Path('tmper').exists()
