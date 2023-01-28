"""
Contains dynamic definitions which cannot be placed inside static files.

For example PROJECT_PATH has to be calculated runtime.
"""
import pathlib
import configparser
from typing import Final

PROJECT_PATH: Final[pathlib.Path] = pathlib.Path('.').absolute()

# Routing data
with open(PROJECT_PATH/'app/routing.ini') as ROUTING_FILE:
	routing: Final[configparser.ConfigParser] = configparser.ConfigParser()
	routing.read_file(ROUTING_FILE)
