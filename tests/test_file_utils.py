from pathlib import Path

from _pytest.fixtures import SubRequest

from common import mkdir_p


def test_mkdir_p(request: SubRequest):
    def finalize_test():
        tempest = Path("tempest")
        if tempest.exists:
            tempest.rmdir()

    request.addfinalizer(finalize_test)
    mkdir_p("tempest")

    assert Path("tempest").exists()
