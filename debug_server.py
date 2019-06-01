#!.venv/bin/python3
"""
Flask Application Server - PYLINT DEBUG
"""
import subprocess
from dotenv import load_dotenv
# flask
from flask import Flask, request
from definitions import PROJECT_PATH
# ------------------------
# Read the configuration
# and override ENVIRONMENT variables with dotenv
load_dotenv(dotenv_path=PROJECT_PATH/'.env.server', override=True)
# ------------------------
APP = Flask(__name__)
# NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable

@APP.route('/', methods=['POST'])
def debug():
    """Endpoint for application debugging with pylint."""
    pylint_args = request.get_json()
    pylint_args[-1] = str(PROJECT_PATH/pylint_args[-1])
    pylint_args.insert(0, '.venv/bin/pylint')
    try:
        debug_info = subprocess.check_output(pylint_args, timeout=20)
    except subprocess.CalledProcessError as err:
        debug_info = err.output
    return debug_info.decode('utf-8')

if __name__ == '__main__':
    pass
