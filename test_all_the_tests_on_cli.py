"""
Run a series of test invocation making sure each test case works with both 'pytest' and 'python -m pytest' and as a
working directory between the project root and the directory containing the test script.
"""
import os
import subprocess
from enum import Enum, auto
from os import PathLike
from pathlib import Path, PurePath
from typing import List, Union, Sequence, Dict, NamedTuple, NewType

PROJECT_PATH: Path = Path(__file__).absolute().parent


class TestCasePaths(NamedTuple):
    """
    A Test Case represents a full path to the test script.  The project root directory is used to derive paths from
    the project root to the script.  Those paths are used to determine the working directory to start each test to
    validate that a test script can be run from any directory between the project's root to the script.

    NOTE: Sub-projects will have different project_roots than the_project(PROJECT_PATH).
    """

    project_root: Path
    # test_case can be a file or directory containing test cases
    full_test_case_path: Path

    def __str__(self):
        return f'{self.project_root}::{self.full_test_case_path.relative_to(self.project_root)}'

    @classmethod
    def gen_test_case_paths(cls, project_root: Path, test_case: Path) -> "TestCasePaths":
        """
        This TestCasePaths generator expects the test_case to be a fragment from the project root to the test script.
        The project_root is prepended to the test_case and provided as the 'TestCasePaths.full_test_case_path'
        value. That path is checked to ensure that a file by that 'full_test_case_path' exits.

        Note: the project_root could be different from the the_project root dir(PROJECT_PATH) for contained
        sub-projects.

        :param project_root:
        :param test_case:
        :return:
        """
        project_root: Path = project_root.absolute()
        full_test_case_path: Path = (project_root / test_case).absolute()
        if not full_test_case_path.exists():
            raise FileNotFoundError(f'Test case {full_test_case_path} does not exist.')

        return TestCasePaths(project_root, full_test_case_path)

    def is_pytest(self) -> bool:
        """
        Determine of the test case is a pytest (a file that begins with 'test_' or a directory)
        :return: True/False
        """
        return (self.full_test_case_path.stem.startswith('test_') or
                self.full_test_case_path.is_dir())

    def is_script(self) -> bool:
        """
        Determine if the test case is a script that is run (not a pytest).
        A script that is simply run by Python is a file that begins with 'run_' and isn't a directory)
        :return: True/False
        """
        return (self.full_test_case_path.stem.startswith('run_') and
                not self.full_test_case_path.is_dir())

    def get_working_directories(self) -> List[Path]:
        """

        :return: list of absolute paths from the project directory to the directory containing the script.
        """
        test_path = self.full_test_case_path
        if not self.full_test_case_path.is_dir():
            # The last 'part' of the path needs to be a directory, not the script.
            test_path = self.full_test_case_path.parent
        # The path fragment between the project_root and the directory containing the script.
        test_path: PurePath = test_path.relative_to(self.project_root)

        # Create a list of full paths for every directory between the project_root and the directory containing the
        # script.
        working_directories: [Path] = [self.project_root]
        for next_part in test_path.parts:
            working_directories.append(self.project_root / next_part)
        return working_directories


class TestType(Enum):
    """
    TestType enum
    """
    PYTEST = auto()
    PYTHON_PYTEST = auto()
    PYTHON = auto()


class RunningTestCase(NamedTuple):
    """
    Named tuple associated with a currently running test case.
    """
    test_type: TestType
    cwd: str
    process: Union[None, subprocess.Popen]

    def __str__(self):
        args: POpenArgs = self.process.args
        which_test_how: str = f'unknown: {args[-1]}'
        if isinstance(args, list):
            args: Sequence = args
            if self.test_type == TestType.PYTHON:
                which_test_how = f'script: {args[-1]}'
            elif self.test_type == TestType.PYTHON_PYTEST:
                which_test_how = f'Python pytest: {args[-1]}'
            elif self.test_type == TestType.PYTEST:
                which_test_how = f'pytest: {args[-1]}'
        return f'{which_test_how} from {self.cwd}'





TESTS: List[TestCasePaths] = [
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_module0.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_package.py')),
    # Path('src/run_the_project_main.py'),
    # Path('run_the_project_main_reusable_func.py'),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('run_just_because_you_can.py'),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('run_the_project_main.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_the_project_main_reusable_func.py')),
]

ENV: Dict[str, str] = os.environ.copy()
ENV.update({'PYTHONDONTWRITEBYTECODE': '-1'})

def _run_pytest(test_type: TestType, work_directory: Path, test_case: TestCasePaths) \
        -> Union[None, RunningTestCase]:
    """
    Run a python script base on the test_type.

    None: is returned if the test_case can't be run with the requested test_type.

    :param test_type: enum to determine if a pytest (or a python-pytest) or a regular runnable script.
    :param work_directory: working directory from whence the script is run
    :param test_case: full path to the script
    :return: a RunningTestCase containing references to the running process(Popen object) and data associated with
    how the process was started.
    """
    if test_case.is_pytest():
        if test_type == TestType.PYTEST:
            command = 'pytest'
        elif test_type == TestType.PYTHON_PYTEST:
            command = 'python -B -m pytest'
        else:
            return None
    elif test_type == TestType.PYTHON and test_case.is_script():
        command = 'python -B'
    else:
        return None

    if work_directory == test_case.project_root:
        work_directory_str = test_case.project_root.relative_to(PROJECT_PATH)
    else:
        work_directory_str = f'{test_case.project_root.relative_to(PROJECT_PATH)}/' \
                             f'{work_directory.relative_to(test_case.project_root)}'

    print(f'Starting: {command} {test_case.full_test_case_path.relative_to(work_directory)} '
          f'from {work_directory_str}')

    command = f'{command} {test_case.full_test_case_path}'
    process: subprocess.Popen = \
        subprocess.Popen(command.split(), cwd=str(work_directory),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         bufsize=1, universal_newlines=True, env=ENV)

    return RunningTestCase(test_type, work_directory_str, process)


POpenArgs = NewType('POpenArgs', Union[bytes, str, Sequence[Union[bytes, str, PathLike]]])


def _run_all_tests() -> None:
    running_test_cases: List[RunningTestCase] = []

    # Start all tests
    for test in TESTS:
        # ... over all test types
        for test_type in TestType:
            # ... changing the work dir from the project root to directory containing script
            for working_directory in test.get_working_directories():
                running_test_case: Union[None, RunningTestCase] = \
                    _run_pytest(test_type, working_directory, test)
                if running_test_case:
                    running_test_cases.append(running_test_case)

    test_count: int = len(running_test_cases)
    tests_passed: int = 0
    # Print them out when each complete (in order)
    for running_test_case in running_test_cases:
        if running_test_case.process.wait() != 0:
            print(f'\nCompleted (w/ error): {running_test_case}\n\t')
            # pylint: disable=expression-not-assigned
            [print(f'\t{line}', end='') for line in running_test_case.process.stdout]
            [print(f'\t{line}', end='') for line in running_test_case.process.stderr]
            # pylint: enable=expression-not-assigned
            break
        print(f'\nCompleted: {running_test_case}\n\t')
        # pylint: disable=expression-not-assigned
        [print(f'\t{line}', end='') for line in running_test_case.process.stdout]
        # pylint: enable=expression-not-assigned

        tests_passed += 1

    if tests_passed == test_count:
        print(f'\nAll {test_count} tests passed!')
    else:
        print(f'\n{test_count} tests out of {test_count} passed ')


if __name__ == '__main__':
    _run_all_tests()
