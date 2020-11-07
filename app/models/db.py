"""Database"""
from typing import Final
from flask_sqlalchemy import SQLAlchemy

DB: Final[SQLAlchemy] = SQLAlchemy()
