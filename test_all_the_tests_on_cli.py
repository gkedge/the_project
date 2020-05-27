import subprocess
from enum import Enum, auto
from os import PathLike
from pathlib import Path
from typing import List, Union, Sequence

TESTS: List[Path] = [
    Path('test_package.py'),
    # Path('src/run_the_project_main.py'),
    # Path('run_the_project_main_reusable_func.py'),
    Path('run_just_because_you_can.py'),
    Path('test_the_project_main_reusable_func.py'),
]


class TestType(Enum):
    PYTEST = auto()
    PYTHON_PYTEST = auto()
    PYTHON = auto()


def _run_pytest(test_type: TestType, test_module_or_directory: Path) -> \
        Union[None, subprocess.Popen]:
    if test_module_or_directory.name.startswith('test_') or test_module_or_directory.is_dir():
        if test_type == TestType.PYTEST:
            command = f'pytest {test_module_or_directory}'
        elif test_type == TestType.PYTHON_PYTEST:
            command = f'python -B  -m pytest {test_module_or_directory}'
        else:
            return None
    elif test_type == TestType.PYTHON and test_module_or_directory.name.startswith('run_'):
        command = f'python -B {test_module_or_directory}'
    else:
        return None

    return subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            bufsize=1, universal_newlines=True)


def _which_tests_how(running_test):
    args: Union[bytes, str, Sequence[Union[bytes, str, PathLike]]] = running_test.args
    which_test_how: str = f'\nArgs: {args}'
    if isinstance(args, list):
        args: Sequence = args
        if 'python' in args:
            if 'pytest' in args:
                which_test_how = f'\nRunning Python pytest: {args[-1]}'
            else:
                which_test_how = f'\nRunning script: {args[-1]}'
        elif 'pytest' in args:
            which_test_how = f'\nRunning pytest: {args[-1]}'
    print(which_test_how)


def _run_all_tests() -> None:
    running_tests: List[subprocess.Popen] = []

    # Start all tests
    for test in TESTS:
        for test_type in TestType:
            popen_obj: Union[None, subprocess.Popen] = _run_pytest(test_type, test)
            if popen_obj:
                running_tests.append(popen_obj)

    test_count: int = len(running_tests)
    tests_passed: int = 0
    # Print them out when each complete (in order)
    for running_test in running_tests:
        if running_test.wait() != 0:
            _which_tests_how(running_test)
            [print(f'\t{line}', end='') for line in running_test.stdout]
            [print(f'\t{line}', end='') for line in running_test.stderr]
            break
        _which_tests_how(running_test)
        [print(f'\t{line}', end='') for line in running_test.stdout]

        tests_passed += 1

    if tests_passed == test_count:
        print(f'\nAll {test_count} tests passed!')


if __name__ == '__main__':
    _run_all_tests()
