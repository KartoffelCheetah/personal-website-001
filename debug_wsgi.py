#!.venv/bin/python3
"""WSGI file for debugger"""
from debug_server import APP

if __name__ == '__main__':
    APP.run()
