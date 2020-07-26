"""
Run a series of test invocation making sure each test case works with both 'pytest' and 'python -m pytest' and as a
working directory between the project root and the directory containing the test script.
"""
import os
import shlex
import subprocess

from enum import Enum, auto, IntEnum
from os import PathLike
from pathlib import Path, PurePath
from typing import List, Union, Sequence, Dict, NamedTuple, NewType, Optional, Tuple


class TestCasePath:
    def __init__(self, project_root: PurePath, test_case: PurePath):
        """
        Note: the project_root could be a subproject's root; not necessarily to run of
        the project leveraging this CLI test runner.
        """
        self._project_root: PurePath = project_root
        self._test_case: PurePath = test_case
        self.check_test_case_path()

    @property
    def project_root(self) -> PurePath:
        return self._project_root

    @property
    def test_case(self) -> PurePath:
        return self._test_case

    @property
    def full_test_case_path(self) -> Path:
        project_root: Path = Path(self._project_root).absolute()
        full_test_case_path: Path = (project_root / self._test_case)
        return full_test_case_path

    @property
    def test_case_relative_to_project_root(self) -> PurePath:
        return self.test_case_relative_to(self.project_root)

    def test_case_relative_to(self, path: PurePath) -> PurePath:
        return self.full_test_case_path.relative_to(path)

    def test_case_relative_to_project(self, path: PurePath) -> PurePath:
        if path == self._project_root:
            test_case_relative_to_project = self._project_root
        else:
            test_case_relative_to_project = self._project_root / path.relative_to(self._project_root)
        return test_case_relative_to_project

    @property
    def is_dir_test_case(self) -> bool:
        return self.full_test_case_path.is_dir()

    def check_test_case_path(self) -> None:
        full_test_case_path: Path = self.full_test_case_path
        if not full_test_case_path.exists():
            raise FileNotFoundError(f'Test case {full_test_case_path} does not exist.')

    @property
    def working_directories(self) -> List[PurePath]:
        """

        :return: list of paths from the project directory to the directory containing the script.
        """
        test_path: PurePath = self.full_test_case_path
        if not self.is_dir_test_case:
            # The last 'part' of the path needs to be a directory, not the script.
            test_path: PurePath = self.full_test_case_path.parent
        # The path fragment between the project_root and the directory containing the script.
        test_path: PurePath = test_path.relative_to(self._project_root)

        # Create a list of full paths for every directory between the project_root and the directory containing the
        # script.
        working_directories: [PurePath] = [self._project_root]
        for next_part in test_path.parts:
            working_directories.append(self._project_root / next_part)
        return working_directories


class Group(IntEnum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()


class TestType(Enum):
    """
    TestType enum
    """
    PYTEST = auto()
    PYTHON_PYTEST = auto()
    PYTHON = auto()

    def is_pytest(self) -> bool:
        return self in [TestType.PYTEST, TestType.PYTHON_PYTEST]

    def python_command(self, is_script: bool) -> Optional[str]:
        command: Optional[str] = None
        if self.is_pytest():
            if self == TestType.PYTEST:
                command = 'pytest'
            else:
                command = 'python -B -m pytest'
        elif is_script:
            command = 'python -B'

        return command

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


class TestCase(NamedTuple):
    """
    A Test Case represents a full path to the test script.  The project root directory is used to derive paths from
    the project root to the script.  Those paths are used to determine the working directory to start each test to
    validate that a test script can be run from any directory between the project's root to the script.
    """

    # full_test_case_path can be a file or directory containing test cases
    test_case_path: TestCasePath
    test_types: Tuple[TestType]
    pytest_filter: str
    group: Group

    def __str__(self):
        return f'{self.test_case_path.project_root}::' \
               f'{self.test_case_path.test_case_relative_to_project_root}'

    @classmethod
    def gen_test_case(cls,
                      test_case_path: TestCasePath,
                      group: Group = Group.ONE,
                      pytest_filter: str = None,
                      test_types: Tuple[TestType, ...] = TestType.all_test_types(),
                      ) -> "TestCase":
        """
        This TestCase generator expects the test_case to be a fragment from the project root to the test script.
        The project_root is prepended to the test_case and provided as the 'TestCase.full_test_case_path'
        value. That path is checked to ensure that a file by that 'full_test_case_path' exits.

        :param test_case_path:
        :param group:
        :param pytest_filter: pytest -k string
        :param test_types:

        :return: test case paths object

        """

        if test_case_path.is_dir_test_case:
            test_types = TestType.only_pytest_types(test_types)

        if pytest_filter and not TestType.is_only_pytest_types(test_types):
            raise RuntimeError(f'filter {pytest_filter} may only be used for pytests.')

        return TestCase(test_case_path, test_types, pytest_filter, group)

    def python_command(self, test_type: TestType) -> Optional[str]:
        command = test_type.python_command(self._is_script)
        if command and test_type.is_pytest() and self.pytest_filter:
            command = f'{command} -k "{self.pytest_filter}"'

        return command

    def test_case_relative_to_cwd(self, working_directory: PurePath) -> PurePath:
        return self.test_case_path.test_case_relative_to(working_directory)

    def cwd_relative_to_project(self, working_directory: PurePath) -> PurePath:
        """
        This method may seem odd, but submodules will have a different project roots
        than the top-level project root.

        :param working_directory: absolute path to cwd
        :return: working directory relative to the test case's project_root
        """

        return self.test_case_path.test_case_relative_to_project(working_directory)

    @property
    def working_directories(self) -> List[PurePath]:
        """

        :return: list of paths from the project directory to the directory containing the script.
        """
        return self.test_case_path.working_directories

    @property
    def _is_script(self) -> bool:
        """
        Determine if the test case is a script that is run (not a pytest).
        A script that is simply run by Python is a file that begins with 'run_' and isn't a directory)
        :return: True/False
        """
        return (self.test_case_path.full_test_case_path.stem.startswith('run_') and
                not self.test_case_path.is_dir_test_case)


ENV: Dict[str, str] = os.environ.copy()
ENV.update({'PYTHONDONTWRITEBYTECODE': '-1'})

POpenArgs = NewType('POpenArgs', Union[bytes, str, Sequence[Union[bytes, str, PathLike]]])


class _RunningTestCase(NamedTuple):
    """
    Named tuple associated with a currently running test case.
    """
    group: Group
    test_type: TestType
    cwd: PurePath
    process: Optional[subprocess.Popen]

    def __str__(self) -> str:
        args: POpenArgs = self.process.args
        which_test_how: str = f'unknown: {args[-1]}'
        if isinstance(args, list):
            args: Sequence = args
            if self.test_type == TestType.PYTHON:
                which_test_how = f'(Group {self.group}) script: {args[-1]}'
            elif self.test_type == TestType.PYTHON_PYTEST:
                which_test_how = f'(Group {self.group}) Python pytest: {args[-1]}'
            elif self.test_type == TestType.PYTEST:
                which_test_how = f'(Group {self.group}) pytest: {args[-1]}'
        return f'{which_test_how} from {self.cwd}'


def _run_pytest(test_type: TestType, work_directory: PurePath, test_case: TestCase) -> Optional[_RunningTestCase]:
    """
    Run a python script base on the test_type.

    None: is returned if the test case can't be run with the requested test_type.

    :param test_type: enum to determine if a pytest (or a python-pytest) or a regular runnable script
    :param work_directory: working directory from whence the script is run
    :param test_case: manage test case paths relative to project root and current working directory
    :return: a _RunningTestCase containing reference to the running process(Popen object) and data associated with
    how the process was started
    """

    command: str = test_case.python_command(test_type)
    if not command:
        return None

    cwd_relative_to_test_case_project: PurePath = test_case.cwd_relative_to_project(work_directory)
    test_case_relative_to_cwd: PurePath = test_case.test_case_relative_to_cwd(work_directory)
    print(f'Starting: {command} {test_case_relative_to_cwd} from {cwd_relative_to_test_case_project}')

    command = f'{command} {test_case_relative_to_cwd}'
    process: subprocess.Popen = \
        subprocess.Popen(shlex.split(command), cwd=str(Path(work_directory).absolute()),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         bufsize=1, universal_newlines=True, env=ENV)

    return _RunningTestCase(test_case.group, test_type, cwd_relative_to_test_case_project, process)


def _get_group_tests(test_case_paths: Tuple[TestCase, ...], group: Group) -> Tuple[TestCase, ...]:
    return tuple(tcp for tcp in test_case_paths if group == tcp.group)


def run_all_tests(test_cases: Tuple[TestCase, ...] = tuple()) -> None:
    running_test_cases: List[_RunningTestCase] = []
    test_count: int = 0
    tests_passed: int = 0

    # Start all tests
    for group in Group:
        for test_case in _get_group_tests(test_cases, group):
            # ... over all test_case types
            for test_type in TestType:
                if test_type not in test_case.test_types:
                    continue
                # ... changing the work dir from the project root to directory containing script
                for working_directory in test_case.working_directories:
                    running_test_case = _run_pytest(test_type, working_directory, test_case)
                    if running_test_case:
                        running_test_cases.append(running_test_case)

        test_count += len(running_test_cases)
        # Print them out when each complete (in order)
        for running_test_case in running_test_cases:
            if running_test_case.process.wait() != 0:
                print(f'\nCompleted (w/ error): {running_test_case}\n\t')
                # pylint: disable=expression-not-assigned
                [print(f'\t{line}', end='') for line in running_test_case.process.stdout]
                # pylint: enable=expression-not-assigned
            print(f'\nCompleted: {running_test_case}\n\t')
            # pylint: disable=expression-not-assigned
            [print(f'\t{line}', end='') for line in running_test_case.process.stdout]
            # pylint: enable=expression-not-assigned

            tests_passed += 1

        running_test_cases.clear()

    if tests_passed == test_count:
        print(f'\nAll {test_count} tests passed!')
    else:
        print(f'\n{tests_passed} tests out of {test_count} passed ')


if __name__ == '__main__':
    project_path: PurePath = Path(__file__).absolute().parent.parent


    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))


    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path('tests/test_can_test_case_import.py'),
                               test_types=(TestType.PYTEST,)),
        TestCase.gen_test_case(gen_test_case_path('tests/test_utils.py')),
        TestCase.gen_test_case(gen_test_case_path('tests/test_file_utils.py'), Group.TWO),
        TestCase.gen_test_case(gen_test_case_path('tests/test_module0.py')),
        TestCase.gen_test_case(gen_test_case_path('tests/test_package.py')),
        TestCase.gen_test_case(gen_test_case_path('tests/test_the_project_main_reusable_func.py')),
        TestCase.gen_test_case(gen_test_case_path('tests'), Group.THREE,
                               pytest_filter='(not test_can_test_case_import_from_root_dir)'),
        TestCase.gen_test_case(gen_test_case_path('src/run_the_project_main.py'), test_types=(TestType.PYTHON,)),
    )

    run_all_tests(all_test_cases)
