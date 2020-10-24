from pathlib import Path

from _pytest.fixtures import SubRequest

from common import create_tmp_directory, mkdir_p, util0


def test_util0():
    assert util0() == "utils.py:util0"


def test_create_tmp_directory(request: SubRequest):
    def finalize_test():
        temper = Path("temper")
        tmp = Path("tmp")
        if temper.exists:
            temper.rmdir()
        if tmp.exists:
            tmp.rmdir()

    request.addfinalizer(finalize_test)
    create_tmp_directory()
    mkdir_p("temper")

    assert Path("temper").exists()
