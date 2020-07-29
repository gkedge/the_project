"""
Run a series of test invocation making sure each test case works with both
 'pytest' and 'python -m pytest'
"""

from pathlib import Path, PurePath
from typing import Tuple

from run_all_the_tests import TestCase, TestCasePath, TestType, run_all_tests

if __name__ == '__main__':
    project_path: PurePath = Path(__file__).absolute().parent


    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))


    TESTS: List[TestCasePaths] = [
        TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_module0.py')),
        TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_package.py')),
        TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('run_the_project_main.py')),
        TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_the_project_main_reusable_func.py')),
    ]

    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path('test_module0.py')),
        TestCase.gen_test_case(gen_test_case_path('test_the_project_main_reusable_func.py')),
        TestCase.gen_test_case(gen_test_case_path('run_the_project_main.py'), test_types=(TestType.PYTHON,)),
    )

    run_all_tests(all_test_cases)
