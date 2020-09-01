from pathlib import Path

from _pytest.fixtures import SubRequest

from common import mkdir_p


def test_mkdir_p(request: SubRequest):
    def finalize_test():
        Path("tmp").rmdir()

    request.addfinalizer(finalize_test)
    mkdir_p("tmp")

    assert Path("tmp").exists()
