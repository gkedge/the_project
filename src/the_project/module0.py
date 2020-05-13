from . import utils


class Module0:
    def __str__(self) -> str:
        return 'module0.py:Module0'

    def func0(self) -> str:
        return f'module0.py:func0 (with help from: {utils.util0()})'
