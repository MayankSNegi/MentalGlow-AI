# __init__.py
from fastapi import FastAPI
from .api import app as main_app

# Optional alias for easier imports
__all__ = ["main_app"]
