from pathlib import Path

from _pytest.fixtures import SubRequest

from common import util0, create_tmp_directory, mkdir_p


def test_util0():
    assert util0() == 'utils.py:util0'


def test_create_tmp_directory(request: SubRequest):
    def finalize_test():
        Path('tmper').rmdir()
        Path('tmp').rmdir()

    request.addfinalizer(finalize_test)
    create_tmp_directory()
    mkdir_p('tmper')

    assert Path('tmper').exists()
