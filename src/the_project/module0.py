from common import util0


class Module0:
    func0_message = f"module0.py:func0 (with help from: {util0()})"

    def __str__(self) -> str:
        return "module0.py:Module0"

    def func0(self) -> str:
        return f"{self}::func0 (with help from: {util0()})"
