"""
Use this 'common' package initializer to publicly expose the 'common' package content of interest
(classes, types, functions, etc) to code outside of the 'common' package. Outside code is then
insulated from 'common' refactoring at the module level.

Outside code dependent upon 'common', imports the 'util0()' w/o module:
from common import util0
"""
from pathlib import Path

from .file_utils import mkdir_p
from .utils import create_tmp_directory, util0

PROJECT_PATH = Path(__file__).parent.parent.absolute()
