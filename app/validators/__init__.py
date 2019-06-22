"""Validation functions"""
from typing import Callable

def length(min_length: int, max_length: int, required_type: any)-> Callable:
    """Length check

    Parameters
    ----------
    min_length : int
        Minimum length of input.
    max_length : int
        Maximum length of input.
    required_type : any
        Type of input.

    Returns
    -------
    Callable
        Validation funtion.

    """
    def validate(inp: any)-> any:
        """validation function"""
        if not isinstance(inp, required_type):
            raise TypeError("Must be of type %s" % (required_type))
        if not min_length <= len(inp) <= max_length:
            raise ValueError(
                "Length of String must be between %i and %i characters"
                % (min_length, max_length))
        return inp
    return validate
