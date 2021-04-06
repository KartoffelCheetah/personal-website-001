"""Controller Utils"""
import os
from typing import Callable
from flask_restx import abort

def _is_enabled(is_enab: bool) -> Callable:
    """Aborts the restx controller when condition is met"""
    def aborter(*args, **kwargs):# pylint: disable=unused-argument
        return abort(404)
    def wrapper(func: Callable) -> Callable:
        return func if is_enab else aborter
    return wrapper

def only_production(func: Callable) -> Callable:
    """Aborts the restx controller in production"""
    return _is_enabled(os.environ['FLASK_ENV'] == 'development')(func)
