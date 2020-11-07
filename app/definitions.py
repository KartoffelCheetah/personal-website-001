"""
Contains dynamic definitions which cannot be placed inside static files.

For example PROJECT_PATH has to be calculated runtime.
"""

import pathlib
import json
from typing import Final

PROJECT_PATH: Final[pathlib.Path] = pathlib.Path('.').absolute()

# Routing data
with open(PROJECT_PATH/'static/routing.json') as ROUTING_FILE:
    ROUTING: Final[dict] = json.load(ROUTING_FILE)
