"""
Run a series of test invocation making sure each test case works with both
 'pytest' and 'python -m pytest'
"""

from pathlib import Path, PurePath
from typing import Tuple

from run_all_the_tests import TestCase, TestCasePath, run_all_tests

if __name__ == '__main__':
    project_path: PurePath = Path(__file__).absolute().parent


    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))


    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path('test_module0.py')),
        TestCase.gen_test_case(gen_test_case_path('test_utils.py'), wait_between_test_types=True),
        TestCase.gen_test_case(gen_test_case_path('test_file_utils.py'), wait_between_test_types=True),
        TestCase.gen_test_case(gen_test_case_path('test_package.py')),
        TestCase.gen_test_case(gen_test_case_path('test_the_project_main_reusable_func.py')),
        TestCase.gen_test_case(gen_test_case_path('src/run_the_project_main.py')),
    )

    run_all_tests(all_test_cases)
