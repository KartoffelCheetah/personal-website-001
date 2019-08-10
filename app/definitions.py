"""
Contains dynamic definitions which cannot be placed inside static files.

For example PROJECT_PATH had to be calculated runtime.
"""

import pathlib
import json

PROJECT_PATH = pathlib.Path('.').absolute()

# Routing data
with open(PROJECT_PATH/'client/src/assets/routing.json') as ROUTING_FILE:
    ROUTING: dict = json.load(ROUTING_FILE)
