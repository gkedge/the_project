import io
import subprocess
from enum import Enum, auto
from typing import List

TESTS: List[str] = ['test_module0.py', 'test_big_project_main.py']


class TestType(Enum):
    PYTEST = auto()
    PYTHON_PYTEST = auto()


def _run_pytest(test_type: TestType, test_module_or_directory: str) -> subprocess.Popen:
    if test_type == TestType.PYTEST:
        command = ['pytest']
    else:
        command = ['python', '-m', 'pytest']

    command.append(test_module_or_directory)
    return subprocess.Popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def _print_stdout(p: subprocess.Popen) -> None:
    for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
        print(f'\t{line}', end='')


def _run_all_tests() -> None:
    running_tests: List[subprocess.Popen] = []

    # Start all tests
    for test in TESTS:
        for test_type in TestType:
            running_tests.append(_run_pytest(test_type, test))

    test_count: int = len(running_tests)
    tests_passed: int = 0
    # Print them out when each complete (in order)
    for running_test in running_tests:
        running_test.wait()
        if running_test.returncode != 0:
            _print_stdout(running_test)
            break
        _print_stdout(running_test)
        tests_passed += 1

    if tests_passed == test_count:
        print('All tests passed!')


if __name__ == '__main__':
    _run_all_tests()
