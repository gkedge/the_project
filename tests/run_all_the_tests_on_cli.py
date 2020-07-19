"""
Run a series of test invocation making sure each test case works with both 'pytest' and 'python -m pytest' and as a
working directory between the project root and the directory containing the test script.
"""
import os
import shlex
import subprocess

from enum import Enum, auto
from os import PathLike
from pathlib import Path, PurePath
import time
from typing import List, Union, Sequence, Dict, NamedTuple, NewType, Optional, Tuple

PROJECT_PATH: Path = Path(__file__).absolute().parent.parent


class TestType(Enum):
    """
    TestType enum
    """
    PYTEST = auto()
    PYTHON_PYTEST = auto()
    PYTHON = auto()

    def is_pytest(self) -> bool:
        return self in [TestType.PYTEST, TestType.PYTHON_PYTEST]

    @staticmethod
    def all_test_types() -> Tuple["TestType", ...]:
        return tuple(test_type for test_type in TestType)

    @staticmethod
    def only_pytest_types(original_types: Tuple["TestType", ...]) -> Tuple["TestType", ...]:
        return tuple(test_type for test_type in original_types if test_type.is_pytest())

    @staticmethod
    def is_only_pytest_types(original_types: Tuple["TestType", ...]) -> bool:
        for test_type in original_types:
            if not test_type.is_pytest():
                return False

        return True


class TestCasePaths(NamedTuple):
    """
    A Test Case represents a full path to the test script.  The project root directory is used to derive paths from
    the project root to the script.  Those paths are used to determine the working directory to start each test to
    validate that a test script can be run from any directory between the project's root to the script.

    NOTE: Sub-projects will have different project_roots than the_project(PROJECT_PATH).
    """

    # full_test_case_path can be a file or directory containing test cases
    full_test_case_path: Path
    test_types: Tuple[TestType]
    project_root: Path
    pytest_filter: str

    def __str__(self):
        return f'{self.project_root}::{self.full_test_case_path.relative_to(self.project_root)}'

    @classmethod
    def gen_test_case_paths(cls, test_case: Path, test_types: Tuple[TestType, ...] = TestType.all_test_types(),
                            project_root: Path = PROJECT_PATH, pytest_filter: str = None) -> "TestCasePaths":
        """
        This TestCasePaths generator expects the test_case to be a fragment from the project root to the test script.
        The project_root is prepended to the test_case and provided as the 'TestCasePaths.full_test_case_path'
        value. That path is checked to ensure that a file by that 'full_test_case_path' exits.

        Note: the project_root could be different from the the_project root dir(PROJECT_PATH) for contained
        sub-projects.

        :param test_case:
        :param test_types:
        :param project_root:
        :param pytest_filter: pytest -k string
        :return: test case paths object
        """
        project_root: Path = project_root.absolute()
        full_test_case_path: Path = (project_root / test_case).absolute()
        if not full_test_case_path.exists():
            raise FileNotFoundError(f'Test case {full_test_case_path} does not exist.')

        if full_test_case_path.is_dir():
            test_types = TestType.only_pytest_types(test_types)

        if pytest_filter and not TestType.is_only_pytest_types(test_types):
            raise RuntimeError(f'filter {pytest_filter} may only be used for pytests.')

        return TestCasePaths(full_test_case_path, test_types, project_root, pytest_filter)

    def is_script(self) -> bool:
        """
        Determine if the test case is a script that is run (not a pytest).
        A script that is simply run by Python is a file that begins with 'run_' and isn't a directory)
        :return: True/False
        """
        return (self.full_test_case_path.stem.startswith('run_') and
                not self.full_test_case_path.is_dir())

    def python_command(self, test_type: TestType) -> Optional[str]:
        command: Optional[str] = None
        if test_type.is_pytest():
            if test_type == TestType.PYTEST:
                command = 'pytest'
            else:
                command = 'python -B -m pytest'
            if self.pytest_filter:
                command = f'{command} -k "{self.pytest_filter}"'
        elif self.is_script():
            command = 'python -B'

        return command

    def test_case_relative_to_cwd(self, working_directory: Path) -> Path:
        return self.full_test_case_path.relative_to(working_directory)

    def cwd_relative_to_project(self, working_directory: Path) -> Path:
        """
        This method may seem odd, but submodules will have a different project roots
        than the top-level project root.

        :param working_directory: absolute path to cwd
        :return: working directory relative to the test case's project_root
        """
        if working_directory == self.project_root:
            work_directory = self.project_root.relative_to(PROJECT_PATH)
        else:
            work_directory = self.project_root.relative_to(PROJECT_PATH) / \
                             working_directory.relative_to(self.project_root)
        return work_directory

    @property
    def working_directories(self) -> List[Path]:
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


ENV: Dict[str, str] = os.environ.copy()
ENV.update({'PYTHONDONTWRITEBYTECODE': '-1'})


class RunningTestCase(NamedTuple):
    """
    Named tuple associated with a currently running test case.
    """
    test_type: TestType
    cwd: Path
    process: Optional[subprocess.Popen]

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
    TestCasePaths.gen_test_case_paths(Path('tests/test_can_test_case_import.py'), (TestType.PYTEST,)),
    TestCasePaths.gen_test_case_paths(Path('tests/test_utils.py')),
    TestCasePaths.gen_test_case_paths(Path('tests/test_file_utils.py')),
    TestCasePaths.gen_test_case_paths(Path('tests/test_module0.py')),
    TestCasePaths.gen_test_case_paths(Path('tests/test_package.py')),
    TestCasePaths.gen_test_case_paths(Path('tests/test_the_project_main_reusable_func.py')),
    TestCasePaths.gen_test_case_paths(Path('tests'), pytest_filter='(not test_can_test_case_import_from_root_dir)'),
    TestCasePaths.gen_test_case_paths(Path('src/run_the_project_main.py'), (TestType.PYTHON,)),
]

ENV: Dict[str, str] = os.environ.copy()
ENV.update({'PYTHONDONTWRITEBYTECODE': '-1'})


def _run_pytest(test_type: TestType, work_directory: Path, test_case_paths: TestCasePaths) -> \
        Optional[RunningTestCase]:
    """
    Run a python script base on the test_type.

    None: is returned if the test case can't be run with the requested test_type.

    :param test_type: enum to determine if a pytest (or a python-pytest) or a regular runnable script
    :param work_directory: working directory from whence the script is run
    :param test_case_paths: manage test case paths relative to project root and current working directory
    :return: a RunningTestCase containing references to the running process(Popen object) and data associated with
    how the process was started
    """

    command: str = test_case_paths.python_command(test_type)
    if not command:
        return

    cwd_relative_to_test_case_project: Path = test_case_paths.cwd_relative_to_project(work_directory)
    test_case_relative_to_cwd = test_case_paths.test_case_relative_to_cwd(work_directory)
    print(f'Starting: {command} {test_case_relative_to_cwd} from {cwd_relative_to_test_case_project}')

    command = f'{command} {test_case_relative_to_cwd}'
    process: subprocess.Popen = \
        subprocess.Popen(shlex.split(command), cwd=str(work_directory),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         bufsize=1, universal_newlines=True, env=ENV)

    return RunningTestCase(test_type, cwd_relative_to_test_case_project, process)


POpenArgs = NewType('POpenArgs', Union[bytes, str, Sequence[Union[bytes, str, PathLike]]])


def _run_all_tests() -> None:
    running_test_cases: List[RunningTestCase] = []

    # Start all tests
    for test in TESTS:
        # ... over all test types
        for test_type in TestType:
            if test_type not in test.test_types:
                continue
            # ... changing the work dir from the project root to directory containing script
            for working_directory in test.working_directories:
                running_test_case: Optional[RunningTestCase] = \
                    _run_pytest(test_type, working_directory, test)
                time.sleep(.1)
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
        print(f'\n{tests_passed} tests out of {test_count} passed ')


if __name__ == '__main__':
    _run_all_tests()
