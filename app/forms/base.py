"""Common parent of parsers.
The arguments added here will be part of all parsers copied from BASE_PARSER"""
from flask_restful import reqparse

BASE_PARSER = reqparse.RequestParser(trim=True)
