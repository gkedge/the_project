"""
Run a series of test invocation making sure each test case works with both
 'pytest' and 'python -m pytest'
"""

from pathlib import Path, PurePath
from typing import Tuple

from run_all_the_tests import Group, TestCase, TestCasePath, TestType, run_all_tests

if __name__ == "__main__":
    project_path: PurePath = Path(__file__).parent.absolute()

    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))

    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(
            gen_test_case_path("tests/test_can_test_case_import.py"),
            test_types=frozenset([TestType.PYTEST]),
        ),
        TestCase.gen_test_case(
            gen_test_case_path("tests/test_file_utils.py"),
            group=Group.TWO,
            wait_between_test_types=True,
        ),
        TestCase.gen_test_case(gen_test_case_path("tests/test_module0.py")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_package.py")),
        TestCase.gen_test_case(gen_test_case_path("tests/test_the_project_main_reusable_func.py")),
        TestCase.gen_test_case(
            gen_test_case_path("tests/test_utils.py"),
            group=Group.THREE,
            wait_between_test_types=True,
        ),
        TestCase.gen_test_case(
            gen_test_case_path("tests"),
            group=Group.FOUR,
            wait_between_test_types=True,
            pytest_filter="(not test_can_test_case_import)",
        ),
        TestCase.gen_test_case(
            gen_test_case_path("src/run_the_project_main.py"),
            test_types=frozenset([TestType.PYTHON]),
        ),
    )

    run_all_tests(all_test_cases)
