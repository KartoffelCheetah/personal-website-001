"""
Contains dynamic definitions which cannot be placed inside static files.

For example PRJECT_PATH had to be calculated runtime.
"""

import pathlib

PROJECT_PATH = pathlib.Path('.').absolute()
