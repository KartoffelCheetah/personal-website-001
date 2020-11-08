"""Database"""
from typing import Final
from flask_sqlalchemy import SQLAlchemy

db: Final[SQLAlchemy] = SQLAlchemy()
