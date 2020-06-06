"""
utils module of, reusable functions.
"""
from . import file_utils


def util0() -> str:
    """
    A reusable function
    :return:
    """
    return 'utils.py:util0'


def create_tmp_directory() -> None:
    file_utils.mkdir_p('tmp')
